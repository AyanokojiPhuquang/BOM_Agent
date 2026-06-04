"""Tool to look up and return datasheet PDF download links for product codes."""

from langchain_core.tools import tool
from loguru import logger
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlmodel import select

from src.db.database import get_manual_db_session
from src.db.models.products import Product


class GetDatasheetInput(BaseModel):
    """Input schema for the get_datasheet_link tool."""

    product_codes: list[str] = Field(
        description="List of product codes to look up datasheets for, e.g. ['SFP-10G-LR', 'CVR-QSFP-SFP10G']"
    )


@tool(args_schema=GetDatasheetInput)
async def get_datasheet_link(product_codes: list[str]) -> str:
    """Look up datasheet PDF download links for one or more product codes.

    Call this tool when a customer asks to download or view the datasheet
    for a specific product. Returns download links for the PDF datasheets.

    Args:
        product_codes: List of product codes/part numbers to find datasheets for.

    Returns:
        Formatted list of download links, or a message if not found.
    """
    if not product_codes:
        return "No product codes provided."

    try:
        async with get_manual_db_session() as session:
            normalized = [c.strip().upper() for c in product_codes]
            result = await session.execute(
                select(Product).where(func.upper(Product.code).in_(normalized))
            )
            products = result.scalars().all()
            product_map = {p.code.strip().upper(): p for p in products}
    except Exception as e:
        logger.error(f"Datasheet lookup failed: {e}")
        return "Unable to look up datasheets at this time."

    lines: list[str] = []
    not_found: list[str] = []
    seen_urls: set[str] = set()

    for code in product_codes:
        key = code.strip().upper()
        product = product_map.get(key)

        if product and product.pdf_url:
            if product.pdf_url not in seen_urls:
                lines.append(f"- **{code}**: [Tải PDF]({product.pdf_url})")
                seen_urls.add(product.pdf_url)
            else:
                lines.append(f"- **{code}**: (cùng datasheet với sản phẩm trên)")
        elif product and product.datasheet_path:
            lines.append(f"- **{code}**: Datasheet có trong hệ thống nhưng chưa có link PDF tải về.")
        else:
            not_found.append(code)

    if not lines and not_found:
        return f"Không tìm thấy datasheet cho: {', '.join(not_found)}. Vui lòng kiểm tra lại mã sản phẩm."

    output_parts: list[str] = []
    if lines:
        output_parts.append("**Datasheet download:**\n" + "\n".join(lines))
    if not_found:
        output_parts.append(f"\n⚠️ Không tìm thấy datasheet cho: {', '.join(not_found)}")

    return "\n".join(output_parts)
