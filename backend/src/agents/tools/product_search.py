"""Product search tool for the sales assistant agent.

Searches products in the database by keyword, code, brand, or category.
"""

from langchain_core.tools import tool
from loguru import logger
from pydantic import BaseModel, Field
import unicodedata

from src.db.database import get_manual_db_session
from sqlalchemy import text


def _normalize(s: str) -> str:
    """Normalize Unicode to NFC form for consistent comparison."""
    return unicodedata.normalize("NFC", s)


class SearchProductsInput(BaseModel):
    query: str = Field(description="Search keyword: product name, code, brand, or category")
    limit: int = Field(default=20, description="Max results to return")


class GetProductInput(BaseModel):
    product_code: str = Field(description="Exact product code")


@tool(args_schema=SearchProductsInput)
async def search_products(query: str, limit: int = 20) -> str:
    """Search products by keyword. Matches against product name, code, brand name, or category.

    Use this tool when a customer asks about products, to find what's available.
    Returns a list of matching products with code, name, price, brand, and category.

    Args:
        query: Search keyword (product name, code, brand, category, etc.)
        limit: Maximum number of results (default 20)
    """
    try:
        async with get_manual_db_session() as session:
            # Split query into words and match ALL words (AND logic)
            words = [_normalize(w.strip()) for w in query.split() if w.strip()]
            if not words:
                return "Vui lòng nhập từ khóa tìm kiếm."

            logger.info(f"Product search: query='{query}', words={words}")

            conditions = []
            params = {"lim": limit}
            for i, word in enumerate(words):
                key = f"w{i}"
                conditions.append(
                    f"(name ILIKE :{key} OR code ILIKE :{key} OR category_name ILIKE :{key} OR brand_name ILIKE :{key})"
                )
                params[key] = f"%{word}%"

            where_clause = " AND ".join(conditions)
            result = await session.execute(
                text(f"""
                    SELECT code, name, sell_price, price, image, category_name, brand_name, unit, available
                    FROM nhanh_products
                    WHERE {where_clause}
                    ORDER BY name
                    LIMIT :lim
                """),
                params,
            )
            rows = result.fetchall()

            if not rows:
                logger.info(f"Product search: no results for '{query}'")
                return f"Không tìm thấy sản phẩm nào khớp với '{query}'."

            lines = [f"Tìm thấy {len(rows)} sản phẩm:"]
            for r in rows:
                code, name, sell_price, base_price, image, category, brand, unit, available = r
                price = sell_price if sell_price else base_price
                price_str = f"{int(price):,}đ" if price else "Liên hệ"
                lines.append(f"- **{code}**: {name} | Thương hiệu: {brand} | Loại: {category} | Giá: {price_str}")

            return "\n".join(lines)

    except Exception as e:
        logger.error(f"Product search failed: {e}")
        return f"Lỗi khi tìm kiếm sản phẩm: {e}"


@tool(args_schema=GetProductInput)
async def get_product_detail(product_code: str) -> str:
    """Get detailed information about a specific product by its exact code.

    Use this when you need full details about a product the customer is interested in.

    Args:
        product_code: The exact product code (e.g. MS885DT2XW, TLG04301V)
    """
    try:
        async with get_manual_db_session() as session:
            result = await session.execute(
                text("""
                    SELECT code, name, sell_price, price, image, description, unit,
                           category_name, brand_name, available, remain
                    FROM nhanh_products
                    WHERE UPPER(TRIM(code)) = UPPER(TRIM(:code))
                """),
                {"code": product_code},
            )
            row = result.fetchone()

            if not row:
                return f"Không tìm thấy sản phẩm với mã '{product_code}'."

            code, name, sell_price, base_price, image, desc, unit, category, brand, available, remain = row
            price = sell_price if sell_price else base_price
            price_str = f"{int(price):,}đ" if price else "Liên hệ"

            lines = [
                f"**Mã SP:** {code}",
                f"**Tên:** {name}",
                f"**Thương hiệu:** {brand}",
                f"**Loại:** {category}",
                f"**Giá bán:** {price_str}",
                f"**ĐVT:** {unit or 'cái'}",
            ]
            if desc:
                lines.append(f"**Mô tả:** {desc[:200]}")
            if image:
                lines.append(f"**Hình ảnh:** {image}")
            lines.append(f"**Tồn kho:** {available} (có sẵn) / {remain} (tổng)")

            return "\n".join(lines)

    except Exception as e:
        logger.error(f"Product detail lookup failed: {e}")
        return f"Lỗi khi tra cứu sản phẩm: {e}"
