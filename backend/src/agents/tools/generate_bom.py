"""BOM generation tool for the BOM assistant agent.

This tool is called by the main conversational agent when it has gathered
enough requirements from the user. It resolves product codes via the database
(which contains structured specs extracted from uploaded PDFs), falls back to
filesystem scan if needed, then runs an LLM subagent to produce a structured
BOM and renders the result as an Excel file.
"""

import asyncio
import re
from pathlib import Path

from langchain_core.tools import tool
from loguru import logger

from src.agents.tools.utils.email_templates import build_bom_email_body
from src.agents.tools.utils.excel_renderer import render_bom_excel
from src.agents.tools.schemas import (
    BomProductItem,
    GenerateBomInput,
    GenerateBomOutput,
)
from src.configs import SETTINGS
from src.db.database import get_manual_db_session
from src.db.models.products import Product
from src.services.email_service import send_email
from src.services.llms.models import llm_invoke
from src.services.prompts.service import get_prompt_service

_OUTPUT_DIR = Path("data/generated_boms")
_MODEL_NAME = "agents/bom_generator/default"
_PROMPT_NAME = "tools.generate_bom"


def _normalize_code(code: str) -> str:
    """Normalize a product code for comparison."""
    return re.sub(r"[\s\-_]+", "", code).lower().strip()


# --- Code → product resolution ---


async def _resolve_products(
    items: list[BomProductItem],
) -> list[dict]:
    """Resolve product codes to Product records from the database.

    Tries exact match first, then normalized/partial match.
    Falls back to filesystem scan if DB has no match.

    Returns a list of dicts, one per item, with keys:
        product_code, product (Product or None), datasheet_path (or None),
        quantity, vendor, device_model, notes, error (or None).
    """
    from sqlalchemy import func
    from sqlmodel import select

    codes = [item.product_code.strip() for item in items]
    code_to_product: dict[str, Product] = {}

    try:
        async with get_manual_db_session() as session:
            # Try exact match by code (case-insensitive)
            normalized_codes = [c.upper() for c in codes]
            result = await session.execute(
                select(Product).where(func.upper(Product.code).in_(normalized_codes))
            )
            for p in result.scalars().all():
                code_to_product[p.code.strip().upper()] = p

            # For codes not found, try partial match
            unmatched = [c for c in codes if c.upper() not in code_to_product]
            if unmatched:
                all_result = await session.execute(
                    select(Product).where(Product.status == 1)
                )
                all_products = all_result.scalars().all()

                for code in unmatched:
                    key = code.upper()
                    key_normalized = _normalize_code(code)
                    for p in all_products:
                        p_code = p.code.strip().upper()
                        p_normalized = _normalize_code(p.code)
                        if (p_code in key or key in p_code or
                            p_normalized == key_normalized or
                            p_normalized in key_normalized or
                            key_normalized in p_normalized):
                            code_to_product[key] = p
                            break
    except Exception as e:
        logger.warning(f"DB lookup for product codes failed: {e}")

    # Build results
    results = []
    datasheets_dir = Path(SETTINGS.datasheets_dir).resolve()

    for item in items:
        key = item.product_code.strip().upper()
        product = code_to_product.get(key)

        entry = {
            "product_code": item.product_code,
            "product": product,
            "datasheet_path": product.datasheet_path if product else None,
            "quantity": item.quantity,
            "vendor": item.vendor,
            "device_model": item.device_model,
            "notes": item.notes,
            "error": None,
        }

        # If not found in DB, try filesystem scan as fallback
        if not product:
            path = _find_in_filesystem(item.product_code, datasheets_dir)
            if path:
                entry["datasheet_path"] = path
            else:
                entry["error"] = (
                    f"Product code '{item.product_code}' not found in the catalog. "
                    "Please verify the product code and try again."
                )

        results.append(entry)

    return results


def _find_in_filesystem(code: str, datasheets_dir: Path) -> str | None:
    """Fallback: scan filesystem for a matching product folder."""
    if not datasheets_dir.exists():
        return None

    normalized = _normalize_code(code)

    for md_file in datasheets_dir.rglob("*.md"):
        relative = md_file.relative_to(datasheets_dir)
        if len(relative.parts) < 2:
            continue
        folder_name = relative.parts[-2]
        if (_normalize_code(folder_name) == normalized or
            folder_name.strip().lower() == code.strip().lower()):
            return str(relative)

    # Try content search
    for md_file in datasheets_dir.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            if code in content or code.replace(" ", "") in content:
                return str(md_file.relative_to(datasheets_dir))
        except Exception:
            pass

    return None


# --- Build product info for LLM ---


def _format_product_specs(product: Product) -> str:
    """Format a Product's specs as readable text for the LLM."""
    lines = []
    if product.brand:
        lines.append(f"Brand: {product.brand}")
    if product.description:
        lines.append(f"Description: {product.description}")
    if product.data_rate:
        lines.append(f"Data Rate: {product.data_rate}")
    if product.fiber_type:
        lines.append(f"Fiber Type: {product.fiber_type}")
    if product.wavelength:
        lines.append(f"Wavelength: {product.wavelength}")
    if product.max_distance:
        lines.append(f"Max Distance: {product.max_distance}")
    if product.connector:
        lines.append(f"Connector: {product.connector}")
    if product.main_device:
        lines.append(f"Main Device (thiết bị chính): {product.main_device}")
    if product.category:
        lines.append(f"Category: {product.category}")
    if product.raw_specs:
        lines.append(f"Additional Specs: {product.raw_specs}")
    return "\n".join(lines)


async def _read_product_file(resolved_item: dict, datasheets_dir: str) -> dict:
    """Build product info from the Products DB (user-edited data is the source of truth)."""
    product: Product | None = resolved_item["product"]

    result = {
        "product_code": resolved_item["product_code"],
        "quantity": resolved_item["quantity"],
        "vendor": resolved_item["vendor"],
        "device_model": resolved_item["device_model"],
        "notes": resolved_item["notes"],
        "product_content": None,
        "error": resolved_item["error"],
    }

    if result["error"]:
        return result

    # Product exists in DB — use structured specs directly (this is user-edited truth)
    if product:
        result["product_content"] = _format_product_specs(product)
    elif resolved_item["datasheet_path"]:
        # Fallback: no DB record but has a datasheet file path
        relative_path = resolved_item["datasheet_path"].lstrip("/")
        full_path = Path(datasheets_dir) / relative_path
        try:
            result["product_content"] = full_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            result["error"] = (
                f"Datasheet file not found for product '{resolved_item['product_code']}'. "
                "The file may have been moved or deleted."
            )
        except Exception as e:
            result["error"] = f"Error reading datasheet for {resolved_item['product_code']}: {e}"

    return result


async def _read_all_product_files(resolved_items: list[dict]) -> list[dict]:
    """Read all product files in parallel."""
    datasheets_dir = str(Path(SETTINGS.datasheets_dir).resolve())
    tasks = [_read_product_file(item, datasheets_dir) for item in resolved_items]
    return await asyncio.gather(*tasks)


# --- LLM subagent ---


def _build_subagent_input(items_with_content: list[dict], bom_input: GenerateBomInput) -> str:
    """Build the user prompt for the BOM subagent from product file contents."""
    sections = []

    sections.append(f"Customer: {bom_input.customer_name}")
    sections.append(f"Phone: {bom_input.customer_phone}")

    sections.append(f"\n## Products ({len(items_with_content)} items)\n")

    for i, item in enumerate(items_with_content, 1):
        sections.append(f"### Item {i}: {item['product_code']}")
        sections.append(f"- Quantity: {item['quantity']}")
        sections.append(f"- Vendor: {item['vendor']}")
        if item["device_model"]:
            sections.append(f"- Device model: {item['device_model']}")
        if item["notes"]:
            sections.append(f"- Notes: {item['notes']}")

        if item["error"]:
            sections.append(f"- Note: No datasheet available for this product. Use the product code and vendor info above to create the line item.")
        elif item["product_content"]:
            sections.append(f"\n**Product file content:**\n```\n{item['product_content']}\n```")

        sections.append("")

    return "\n".join(sections)


async def _invoke_bom_subagent(user_prompt: str) -> GenerateBomOutput:
    """Call the LLM subagent to produce structured BOM output."""
    prompt_service = get_prompt_service()
    system_prompt = prompt_service.get_prompt(_PROMPT_NAME, use_local_only=True)

    if not system_prompt:
        raise RuntimeError(f"BOM generation prompt not found: {_PROMPT_NAME}")

    return await llm_invoke(
        model_name=_MODEL_NAME,
        schema=GenerateBomOutput,
        user_prompt=user_prompt,
        system_prompt=system_prompt,
    )


# --- Excel + download ---


def _generate_excel(bom: GenerateBomOutput) -> Path | None:
    """Render BOM to Excel. Returns filepath or None on error."""
    try:
        return render_bom_excel(bom, _OUTPUT_DIR)
    except Exception as e:
        logger.error(f"Excel generation error: {e}")
        return None


# --- Email ---


async def _send_bom_email(bom: GenerateBomOutput, filepath: Path | None) -> bool:
    """Send BOM email to internal team. Returns True if sent."""
    if not SETTINGS.bom_recipient_email:
        return False

    try:
        email_body = build_bom_email_body(bom)
        await send_email(
            to_email=SETTINGS.bom_recipient_email,
            subject=f"BOM — {bom.customer_name} | Starlinks",
            body=email_body,
            is_html=True,
            attachment_path=filepath,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to email BOM: {e}")
        return False


# --- Response formatting ---


def _format_validation_issues(bom: GenerateBomOutput) -> str:
    """Format validation issues as a readable string for the agent."""
    lines = ["**BOM generation could not be completed.** The following issues were found:\n"]
    for issue in bom.validation_issues:
        icon = "❌" if issue.severity == "error" else "⚠️"
        lines.append(f"- {icon} **{issue.field}**: {issue.message}")
    lines.append("\nPlease ask the customer for the missing information and try again.")
    return "\n".join(lines)


def _format_bom_summary(bom: GenerateBomOutput) -> str:
    """Format a successful BOM as a readable summary for the agent."""
    lines = [f"**BOM Generated Successfully** — {bom.customer_name}\n"]

    if bom.customer_phone:
        lines.append(f"Phone: {bom.customer_phone}\n")

    lines.append("| # | SKU | Description | Thiết bị chính | Qty | Price |")
    lines.append("|---|-----|-------------|----------------|-----|-------|")
    for item in bom.line_items:
        price = f"${item.unit_price_usd:.2f}" if item.unit_price_usd else "—"
        lines.append(f"| {item.line} | {item.sku} | {item.description} | {item.vendor_compatibility} | {item.quantity} | {price} |")

    if bom.assumptions:
        lines.append("\n**Assumptions:**")
        for assumption in bom.assumptions:
            lines.append(f"- {assumption}")

    lines.append(f"\n{bom.summary}")

    return "\n".join(lines)


def _build_tool_response(
    bom: GenerateBomOutput,
    email_sent: bool,
    filepath: Path | None = None,
) -> str:
    """Assemble the final tool response from all parts."""
    parts = [_format_bom_summary(bom)]

    if filepath:
        filename = filepath.name
        parts.append(f"\n**Download:** [{filename}](/api/files/boms/{filename})")

    email_note = "Internal email sent." if email_sent else "Internal email not sent."
    parts.append(f"\n_{email_note}_")

    return "\n".join(parts)


# --- Main tool ---


@tool(args_schema=GenerateBomInput)
async def generate_bom(
    customer_name: str,
    customer_phone: str,
    items: list[dict],
) -> str:
    """Generate a structured BOM (Bill of Materials) from selected products.

    Call this tool when you have identified the exact products the customer
    needs. Requires customer name, phone number, and product details.

    Args:
        customer_name: Customer or company name (required).
        customer_phone: Customer phone number (required).
        items: List of products, each with product_code, quantity, vendor,
               and optionally device_model and notes.

    Returns:
        BOM summary with line items and download link,
        or validation issues if something is wrong.
    """

    bom_input = GenerateBomInput(
        customer_name=customer_name,
        customer_phone=customer_phone,
        items=items,
    )

    # Gate: validate that product_codes are real SKUs, not descriptions.
    # Real product codes are short (≤40 chars) and don't contain commas, parentheses, or long spaces.
    # Descriptions are long and verbose.
    invalid_items = []
    for item in bom_input.items:
        code = item.product_code.strip()
        # A real product code: short, no commas, no Vietnamese words
        has_comma = "," in code
        too_long = len(code) > 40
        has_spaces_in_middle = "  " in code or len(code.split()) > 5
        if has_comma or too_long or has_spaces_in_middle:
            invalid_items.append(code)

    if invalid_items:
        lines = ["❌ **Không thể tạo BOM** — Các mục sau không phải là mã sản phẩm hợp lệ:\n"]
        for code in invalid_items:
            lines.append(f"- `{code[:80]}...`" if len(code) > 80 else f"- `{code}`")
        lines.append(
            "\n**Vui lòng cung cấp mã sản phẩm chính xác** (ví dụ: `SFP-25G-LR`, `PC-LC-LC-D-X-LM`, `QSFP-100G-SR4`) "
            "thay vì mô tả sản phẩm.\n\n"
            "Em sẽ tìm mã sản phẩm phù hợp trong catalog — anh/chị vui lòng mô tả yêu cầu và em sẽ tư vấn mã SP đúng nhé."
        )
        return "\n".join(lines)

    # 1. Resolve product codes via database + filesystem fallback
    resolved_items = await _resolve_products(bom_input.items)

    # Check if ALL codes failed to resolve — still proceed but note the errors
    not_found = [r for r in resolved_items if r["error"] and "not found" in r["error"]]
    if not_found and len(not_found) == len(resolved_items):
        logger.info(f"No products found in catalog, proceeding with raw info: {[r['product_code'] for r in resolved_items]}")

    # 2. Read product specs (from DB structured data + markdown files)
    items_with_content = await _read_all_product_files(resolved_items)

    # 3. Call LLM subagent
    user_prompt = _build_subagent_input(items_with_content, bom_input)
    try:
        bom_output = await _invoke_bom_subagent(user_prompt)
    except Exception as e:
        logger.error(f"BOM subagent error: {e}")
        return f"Error generating BOM: {e}. Please try again."

    if not bom_output.is_valid and not bom_output.line_items:
        return _format_validation_issues(bom_output)

    # 4. Inject customer info into BOM output
    bom_output.customer_name = bom_input.customer_name
    bom_output.customer_phone = bom_input.customer_phone

    # 5. Generate Excel
    filepath = _generate_excel(bom_output)

    # 6. Send email
    email_sent = await _send_bom_email(bom_output, filepath)

    # 7. Build response
    return _build_tool_response(bom_output, email_sent, filepath)
