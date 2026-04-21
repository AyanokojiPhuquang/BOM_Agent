"""Real-time inventory checking via Nhanh API.

Given a product code, resolves it to a NhanhProduct via the code field
and fetches live stock levels.
"""

from langchain_core.tools import tool
from loguru import logger

from src.agents.tools.schemas import CheckInventoryInput, ProductInventoryStatus, STATUS_LABELS
from src.app.schemas.nhanh import NhanhProductSearchRequest
from src.db.database import get_manual_db_session
from src.db.models.nhanh import NhanhProduct
from src.db.repositories.nhanh import NhanhProductRepository, NhanhTokenRepository
from src.services.nhanh.service import NhanhService


async def _find_nhanh_products(
    product_repo: NhanhProductRepository,
    codes: list[str],
) -> dict[str, NhanhProduct]:
    """Look up NhanhProducts by code. Returns {uppercase_code: NhanhProduct}."""
    products = await product_repo.get_by_codes(codes)
    return {p.code.strip().upper(): p for p in products if p.code}


async def _fetch_inventory(
    nhanh_service: NhanhService,
    nhanh_ids: list[int],
) -> tuple[dict[int, tuple[int, int]], str | None]:
    """Fetch inventory via product/list endpoint. Returns ({nhanh_id: (available, remain)}, error_msg)."""
    if not nhanh_ids:
        return {}, None

    try:
        response = await nhanh_service.search_products(
            NhanhProductSearchRequest(ids=nhanh_ids, page_size=100)
        )
        return {
            item.id: (item.available, item.remain)
            for item in response.items
        }, None
    except Exception as e:
        logger.warning(f"Nhanh product list API call failed: {e}")
        return {}, str(e)


def _build_status(
    product_code: str,
    quantity: int,
    nhanh_product: NhanhProduct | None,
    inventory: dict[int, tuple[int, int]],
    api_error: str | None = None,
) -> ProductInventoryStatus:
    """Build a single ProductInventoryStatus from DB + API data."""
    if not nhanh_product:
        return ProductInventoryStatus(
            product_code=product_code,
            quantity_requested=quantity,
            status_label="no_data",
        )

    if api_error:
        return ProductInventoryStatus(
            product_code=product_code,
            nhanh_product_name=nhanh_product.name,
            nhanh_id=nhanh_product.nhanh_id,
            quantity_requested=quantity,
            status_label="error",
            error_message=f"Could not check live inventory: {api_error}",
        )

    inv = inventory.get(nhanh_product.nhanh_id)
    if inv is None:
        return ProductInventoryStatus(
            product_code=product_code,
            nhanh_product_name=nhanh_product.name,
            nhanh_id=nhanh_product.nhanh_id,
            quantity_requested=quantity,
            status_label="error",
            error_message="Product exists but inventory data was not returned by Nhanh.",
        )

    available, remain = inv
    if available >= quantity:
        status_label = "in_stock"
    elif available > 0:
        status_label = "partial"
    else:
        status_label = "out_of_stock"

    return ProductInventoryStatus(
        product_code=product_code,
        nhanh_product_name=nhanh_product.name,
        nhanh_id=nhanh_product.nhanh_id,
        quantity_requested=quantity,
        available=available,
        remain=remain,
        is_sufficient=available >= quantity,
        status_label=status_label,
    )


async def check_inventory(codes: list[str], quantities: list[int]) -> list[ProductInventoryStatus]:
    """Check real-time inventory for each product code. Never raises.

    Tries Nhanh API first; falls back to local DB stock data if the API
    is unavailable (e.g. no token, network error).
    """
    try:
        async with get_manual_db_session() as session:
            product_repo = NhanhProductRepository(session)
            token_repo = NhanhTokenRepository(session)
            nhanh_service = NhanhService(token_repo)

            nhanh_by_code = await _find_nhanh_products(product_repo, codes)

            nhanh_ids = [p.nhanh_id for p in nhanh_by_code.values()]
            inventory, api_error = await _fetch_inventory(nhanh_service, nhanh_ids)

            # Fallback: if API failed, use local DB remain/available
            if api_error and not inventory:
                inventory = {
                    p.nhanh_id: (p.available, p.remain)
                    for p in nhanh_by_code.values()
                }
                api_error = None  # Clear error since we have local data

            return [
                _build_status(
                    code,
                    qty,
                    nhanh_by_code.get(code.strip().upper()),
                    inventory,
                    api_error,
                )
                for code, qty in zip(codes, quantities)
            ]

    except Exception as e:
        logger.warning(f"Inventory check failed: {e}")
        return [
            ProductInventoryStatus(
                product_code=code,
                quantity_requested=qty,
                status_label="error",
                error_message=f"Inventory check failed: {e}",
            )
            for code, qty in zip(codes, quantities)
        ]


def _format_status(s: ProductInventoryStatus) -> str:
    """Format a single inventory status as a readable string."""
    label = STATUS_LABELS.get(s.status_label, s.status_label)
    if s.status_label == "partial":
        label = f"Partial (need {s.quantity_requested}, have {s.available})"

    name = s.nhanh_product_name or s.product_code

    lines = [
        f"**Product:** {name}",
        f"**Code:** {s.product_code}",
        f"**Requested:** {s.quantity_requested}",
        f"**Available:** {s.available}",
        f"**In Stock (remain):** {s.remain}",
        f"**Status:** {label}",
    ]
    if s.nhanh_id:
        lines.append(f"**Nhanh ID:** {s.nhanh_id}")
    if s.error_message:
        lines.append(f"**Error:** {s.error_message}")

    return "\n".join(lines)


@tool(args_schema=CheckInventoryInput)
async def check_product_inventory(
    product_code: str,
    quantity: int = 1,
) -> str:
    """Check real-time inventory for a product.

    Call this tool to check when a customer asks about availability.
    Requires the product code (part number).

    Args:
        product_code: Product code/part number, e.g. SFP-10G-ER, SFP-10G-ZR-I
        quantity: Number of units to check availability for.

    Returns:
        Inventory status including available stock and whether
        the requested quantity can be fulfilled.
    """
    statuses = await check_inventory([product_code], [quantity])

    if not statuses:
        return f"Unable to check inventory for {product_code}."

    return _format_status(statuses[0])
