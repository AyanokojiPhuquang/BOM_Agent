"""BOM generation tool for the BOM assistant agent.

This tool is called by the main conversational agent when it has gathered
enough requirements from the user. It resolves product codes to datasheet
files via the database, reads the actual product files from the catalog,
then runs an LLM subagent to produce a structured BOM and renders the
result as an Excel file.
"""

import asyncio
from pathlib import Path

from langchain_core.tools import tool
from loguru import logger

from src.agents.tools.utils.email_templates import build_bom_email_body
from src.agents.tools.utils.excel_renderer import render_bom_excel
from src.agents.tools.inventory_checker import check_inventory
from src.agents.tools.schemas import (
    BomProductItem,
    GenerateBomInput,
    GenerateBomOutput,
    ProductInventoryStatus,
    STATUS_LABELS,
)
from src.configs import SETTINGS
from src.db.database import get_manual_db_session
from src.db.repositories.nhanh import NhanhProductRepository
from src.services.email_service import send_email
from src.services.llms.models import llm_invoke
from src.services.prompts.service import get_prompt_service

_OUTPUT_DIR = Path("data/generated_boms")
_MODEL_NAME = "agents/bom_generator/default"
_PROMPT_NAME = "tools.generate_bom"

_STATUS_ICONS = {
    "in_stock": "V",
    "partial": "!",
    "out_of_stock": "X",
    "no_data": "?",
    "error": "!",
}


# --- Code → file path resolution ---


async def _resolve_product_paths(
    items: list[BomProductItem],
) -> list[dict]:
    """Resolve product codes to datasheet file paths via the database.

    Returns a list of dicts, one per item, with keys:
        product_code, datasheet_path (or None), quantity, vendor,
        device_model, notes, error (or None).
    """
    codes = [item.product_code for item in items]

    code_to_path: dict[str, str | None] = {}
    try:
        async with get_manual_db_session() as session:
            repo = NhanhProductRepository(session)
            products = await repo.get_by_codes(codes)
            for p in products:
                code_to_path[p.code.strip().upper()] = p.datasheet_path
    except Exception as e:
        logger.warning(f"DB lookup for product codes failed: {e}")

    results = []
    for item in items:
        key = item.product_code.strip().upper()
        path = code_to_path.get(key)

        entry = {
            "product_code": item.product_code,
            "datasheet_path": path,
            "quantity": item.quantity,
            "vendor": item.vendor,
            "device_model": item.device_model,
            "notes": item.notes,
            "error": None,
        }

        if key not in code_to_path:
            entry["error"] = (
                f"Product code '{item.product_code}' not found in our database. "
                "Please verify the product code and try again."
            )
        elif not path:
            entry["error"] = (
                f"Product code '{item.product_code}' exists in our system but has no "
                "datasheet linked. The BOM may be missing detailed specs for this item."
            )

        results.append(entry)

    return results


# --- File reading ---


async def _read_product_file(resolved_item: dict, datasheets_dir: str) -> dict:
    """Read a single product file and return its content with item metadata."""
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

    relative_path = resolved_item["datasheet_path"].lstrip("/")
    full_path = Path(datasheets_dir) / relative_path

    try:
        result["product_content"] = full_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        result["error"] = (
            f"Datasheet file not found for product '{resolved_item['product_code']}'. "
            "The file may have been moved or deleted."
        )
        logger.warning(result["error"])
    except Exception as e:
        result["error"] = f"Error reading datasheet for {resolved_item['product_code']}: {e}"
        logger.error(result["error"])

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
            sections.append(f"- ERROR: {item['error']}")
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


def _generate_excel(
    bom: GenerateBomOutput,
    inventory_statuses: list[ProductInventoryStatus],
) -> Path | None:
    """Render BOM to Excel. Returns filepath or None on error."""
    try:
        return render_bom_excel(bom, _OUTPUT_DIR, inventory_statuses=inventory_statuses)
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

    lines.append("| # | SKU | Description | Vendor | Qty | Price |")
    lines.append("|---|-----|-------------|--------|-----|-------|")
    for item in bom.line_items:
        price = f"${item.unit_price_usd:.2f}" if item.unit_price_usd else "—"
        lines.append(f"| {item.line} | {item.sku} | {item.description} | {item.vendor_compatibility} | {item.quantity} | {price} |")

    if bom.assumptions:
        lines.append("\n**Assumptions:**")
        for assumption in bom.assumptions:
            lines.append(f"- {assumption}")

    lines.append(f"\n{bom.summary}")

    return "\n".join(lines)


def _format_inventory_status(statuses: list[ProductInventoryStatus]) -> str:
    """Format inventory statuses as a markdown table."""
    if not statuses:
        return ""

    lines = ["\n## Inventory Status\n"]
    lines.append("| Product | Requested | Available | In Stock | Status |")
    lines.append("|---------|-----------|-----------|----------|--------|")

    for s in statuses:
        name = s.nhanh_product_name or s.product_code
        label = STATUS_LABELS.get(s.status_label, s.status_label)
        if s.status_label == "partial":
            label = f"Partial (need {s.quantity_requested}, have {s.available})"
        icon = _STATUS_ICONS.get(s.status_label, "?")
        lines.append(f"| {name} | {s.quantity_requested} | {s.available} | {s.remain} | {icon} {label} |")

    return "\n".join(lines)


def _build_tool_response(
    bom: GenerateBomOutput,
    inventory_statuses: list[ProductInventoryStatus],
    email_sent: bool,
    filepath: Path | None = None,
) -> str:
    """Assemble the final tool response from all parts."""
    parts = [_format_bom_summary(bom)]

    inventory_section = _format_inventory_status(inventory_statuses)
    if inventory_section:
        parts.append(inventory_section)

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
        BOM summary with line items, download link, and inventory status,
        or validation issues if something is wrong.
    """

    bom_input = GenerateBomInput(
        customer_name=customer_name,
        customer_phone=customer_phone,
        items=items,
    )

    # 1. Resolve product codes to file paths via database
    resolved_items = await _resolve_product_paths(bom_input.items)

    # Check if ALL codes failed to resolve
    not_found = [r for r in resolved_items if r["error"] and "not found in our database" in r["error"]]
    if not_found and len(not_found) == len(resolved_items):
        codes = ", ".join(r["product_code"] for r in not_found)
        return (
            f"Could not find any of the provided product codes in our database: {codes}. "
            "Please verify the product codes and try again."
        )

    # 2. Read product files
    items_with_content = await _read_all_product_files(resolved_items)

    errors = [r for r in items_with_content if r["error"]]
    if errors and all(r["error"] for r in items_with_content):
        error_details = "; ".join(r["error"] for r in errors)
        return f"Could not read any product files: {error_details}. Please verify the product codes."

    # 3. Call LLM subagent
    user_prompt = _build_subagent_input(items_with_content, bom_input)
    try:
        bom_output = await _invoke_bom_subagent(user_prompt)
    except Exception as e:
        logger.error(f"BOM subagent error: {e}")
        return f"Error generating BOM: {e}. Please try again."

    if not bom_output.is_valid:
        return _format_validation_issues(bom_output)

    # 4. Check inventory
    codes = [item.product_code for item in bom_input.items]
    quantities = [item.quantity for item in bom_input.items]
    inventory_statuses = await check_inventory(codes, quantities)

    # 5. Inject customer info into BOM output for downstream use
    bom_output.customer_name = bom_input.customer_name
    bom_output.customer_phone = bom_input.customer_phone

    # 6. Generate Excel
    filepath = _generate_excel(bom_output, inventory_statuses)

    # 7. Send email
    email_sent = await _send_bom_email(bom_output, filepath)

    # 8. Build response
    return _build_tool_response(bom_output, inventory_statuses, email_sent, filepath)
