"""Quotation/BOM generation tool.

Called by the agent when it has gathered enough info from the customer.
Resolves product codes via the database, builds a structured quotation,
and renders the result as an Excel file using the MVC template.
"""

from pathlib import Path

from langchain_core.tools import tool
from loguru import logger
from sqlalchemy import text

from src.agents.tools.utils.excel_renderer import render_bom_excel
from src.agents.tools.schemas import (
    BomLineItem,
    BomProductItem,
    GenerateBomInput,
    GenerateBomOutput,
)
from src.configs import SETTINGS
from src.db.database import get_manual_db_session

_OUTPUT_DIR = Path("data/generated_boms")


async def _resolve_products(items: list[BomProductItem]) -> list[dict]:
    """Look up product codes in DB and return product info."""
    codes = [item.product_code.strip() for item in items]
    results = []

    try:
        async with get_manual_db_session() as session:
            for item in items:
                code = item.product_code.strip()
                row = await session.execute(
                    text("""
                        SELECT code, name, price, sell_price, image,
                               description, unit, category_name, brand_name,
                               available, remain
                        FROM nhanh_products
                        WHERE UPPER(TRIM(code)) = UPPER(TRIM(:code))
                    """),
                    {"code": code},
                )
                product = row.fetchone()

                if product:
                    (p_code, p_name, p_price, p_sell, p_image,
                     p_desc, p_unit, p_cat, p_brand, p_avail, p_remain) = product
                    results.append({
                        "product_code": p_code,
                        "product_name": p_name,
                        "unit_price": float(p_sell) if p_sell else float(p_price) if p_price else 0,
                        "image_url": p_image or "",
                        "description": p_desc or "",
                        "unit": p_unit or "cái",
                        "category": p_cat or "",
                        "brand": p_brand or "",
                        "quantity": item.quantity,
                        "notes": item.notes,
                        "found": True,
                    })
                else:
                    results.append({
                        "product_code": code,
                        "product_name": code,
                        "unit_price": 0,
                        "image_url": "",
                        "description": "",
                        "unit": "cái",
                        "category": "",
                        "brand": "",
                        "quantity": item.quantity,
                        "notes": item.notes,
                        "found": False,
                    })
    except Exception as e:
        logger.warning(f"DB lookup failed: {e}")
        for item in items:
            results.append({
                "product_code": item.product_code,
                "product_name": item.product_code,
                "unit_price": 0,
                "image_url": "",
                "quantity": item.quantity,
                "notes": item.notes,
                "found": False,
            })

    return results


def _build_bom_output(
    bom_input: GenerateBomInput,
    resolved: list[dict],
) -> GenerateBomOutput:
    """Build a GenerateBomOutput from resolved product data."""
    line_items = []
    not_found = []

    for idx, r in enumerate(resolved):
        if not r["found"]:
            not_found.append(r["product_code"])

        line_items.append(BomLineItem(
            line=idx + 1,
            product_code=r["product_code"],
            product_name=r["product_name"],
            image_url=r["image_url"],
            category=r.get("category", ""),
            description=r.get("description", ""),
            quantity=r["quantity"],
            unit=r.get("unit", "cái"),
            unit_price=r["unit_price"],
            discount_percent=0,
            notes=r["notes"] or ("Không tìm thấy trong hệ thống" if not r["found"] else None),
        ))

    assumptions = []
    if not_found:
        assumptions.append(f"Không tìm thấy mã sản phẩm: {', '.join(not_found)}")

    total = sum(item.unit_price * item.quantity for item in line_items)
    summary_lines = [f"Báo giá cho {bom_input.customer_name}:"]
    for item in line_items:
        price_str = f"{int(item.unit_price):,}đ" if item.unit_price else "Liên hệ"
        summary_lines.append(f"- {item.product_code}: {item.product_name} x{item.quantity} @ {price_str}")
    summary_lines.append(f"Tổng: {int(total):,}đ")

    return GenerateBomOutput(
        is_valid=True,
        customer_name=bom_input.customer_name,
        customer_phone=bom_input.customer_phone,
        customer_email=bom_input.customer_email,
        customer_address=bom_input.customer_address,
        line_items=line_items,
        assumptions=assumptions,
        summary="\n".join(summary_lines),
    )


def _format_bom_summary(bom: GenerateBomOutput) -> str:
    """Format BOM as a readable summary."""
    lines = [f"**Báo giá — {bom.customer_name}**\n"]
    lines.append("| # | Mã SP | Tên sản phẩm | SL | Đơn giá | Thành tiền |")
    lines.append("|---|-------|-------------|---:|--------:|-----------:|")

    total = 0
    for item in bom.line_items:
        subtotal = item.unit_price * item.quantity
        total += subtotal
        price_str = f"{int(item.unit_price):,}" if item.unit_price else "Liên hệ"
        sub_str = f"{int(subtotal):,}" if subtotal else "-"
        lines.append(f"| {item.line} | {item.product_code} | {item.product_name} | {item.quantity} | {price_str} | {sub_str} |")

    lines.append(f"\n**Tổng giá trị: {int(total):,}đ**")
    return "\n".join(lines)


def _build_tool_response(bom: GenerateBomOutput, filepath: Path | None = None) -> str:
    """Assemble the final tool response."""
    parts = [_format_bom_summary(bom)]

    if bom.assumptions:
        parts.append("\n⚠️ " + "; ".join(bom.assumptions))

    if filepath:
        filename = filepath.name
        download_link = f"/api/files/boms/{filename}"
        parts.append(f"\n📥 **Tải file báo giá:** [{filename}]({download_link})")
        parts.append(f"\n(QUAN TRỌNG: Khi trả lời khách, hãy copy NGUYÊN link download ở trên, KHÔNG tự tạo link mới)")

    return "\n".join(parts)


@tool(args_schema=GenerateBomInput)
async def generate_bom(
    customer_name: str,
    customer_phone: str,
    items: list[dict],
    customer_email: str = "",
    customer_address: str = "",
) -> str:
    """Generate a quotation (BOM) from selected products.

    Call this tool when you have identified the exact products and quantities.
    Requires customer name, phone number, and product details.

    Args:
        customer_name: Customer or company name (required).
        customer_phone: Customer phone number (required).
        items: List of products, each with product_code, quantity, and optionally notes.
        customer_email: Customer email (optional).
        customer_address: Customer address (optional).

    Returns:
        Quotation summary with line items and download link.
    """
    bom_input = GenerateBomInput(
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_email=customer_email,
        customer_address=customer_address,
        items=items,
    )

    # 1. Resolve product codes from DB
    resolved = await _resolve_products(bom_input.items)

    # Check if ALL codes failed
    not_found = [r for r in resolved if not r["found"]]
    if not_found and len(not_found) == len(resolved):
        codes = ", ".join(r["product_code"] for r in not_found)
        return f"Không tìm thấy mã sản phẩm nào trong hệ thống: {codes}. Vui lòng kiểm tra lại mã sản phẩm."

    # 2. Build structured output
    bom_output = _build_bom_output(bom_input, resolved)

    # 3. Generate Excel
    try:
        filepath = render_bom_excel(bom_output, _OUTPUT_DIR)
    except Exception as e:
        logger.error(f"Excel generation error: {e}")
        filepath = None

    # 4. Build response
    return _build_tool_response(bom_output, filepath)
