"""Real-time inventory checking via Nhanh API.

Given a product code, resolves it to a NhanhProduct via the code field
and fetches live stock levels. If no local Nhanh token is available,
falls back to proxying through the production server.
"""

import httpx
from langchain_core.tools import tool
from loguru import logger

from src.agents.tools.schemas import CheckInventoryInput, ProductInventoryStatus, STATUS_LABELS
from src.app.schemas.nhanh import NhanhProductSearchRequest
from src.configs import SETTINGS
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
    product_codes: list[str] | None = None,
) -> tuple[dict[str, tuple[int, int]], str | None]:
    """Fetch inventory. Returns ({product_code_upper: (available, remain)}, error_msg).

    Tries local Nhanh token first, falls back to production proxy searching by name/code.
    """
    if not nhanh_ids and not product_codes:
        return {}, None

    # Try local Nhanh API first (by nhanh_id)
    real_ids = [nid for nid in nhanh_ids if nid < 40000000]
    if real_ids:
        try:
            response = await nhanh_service.search_products(
                NhanhProductSearchRequest(ids=real_ids, page_size=100)
            )
            return {
                item.code.strip().upper(): (item.available, item.remain)
                for item in response.items
            }, None
        except Exception as e:
            logger.warning(f"Local Nhanh API failed: {e}")

    # Fallback: proxy through production server, search by product code
    proxy_url = SETTINGS.nhanh.proxy_url
    if not proxy_url or not product_codes:
        return {}, None

    result_map: dict[str, tuple[int, int]] = {}
    try:
        for code in product_codes:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(
                    f"{proxy_url}/api/nhanh/products",
                    json={"name": code.strip()},
                    headers={"User-Agent": "StarlinksAgent/1.0"},
                )
                if resp.status_code != 200:
                    continue
                data = resp.json()

            for item in data.get("items", []):
                item_code = item.get("code", "").strip().upper()
                # Match if codes are similar
                if code.strip().upper() in item_code or item_code in code.strip().upper():
                    result_map[code.strip().upper()] = (
                        item.get("available", 0),
                        item.get("remain", 0),
                    )
                    break

        return result_map, None
    except Exception as e:
        logger.warning(f"Production proxy failed: {e}")
        return {}, str(e)


def _build_status(
    product_code: str,
    quantity: int,
    nhanh_product: NhanhProduct | None,
    inventory: dict[str, tuple[int, int]],
    api_error: str | None = None,
) -> ProductInventoryStatus:
    """Build a single ProductInventoryStatus from DB + API data."""
    code_upper = product_code.strip().upper()

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

    inv = inventory.get(code_upper)
    if inv is None:
        return ProductInventoryStatus(
            product_code=product_code,
            nhanh_product_name=nhanh_product.name,
            nhanh_id=nhanh_product.nhanh_id,
            quantity_requested=quantity,
            status_label="no_data",
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
    """Check real-time inventory for each product code. Never raises."""
    try:
        async with get_manual_db_session() as session:
            product_repo = NhanhProductRepository(session)
            token_repo = NhanhTokenRepository(session)
            nhanh_service = NhanhService(token_repo)

            nhanh_by_code = await _find_nhanh_products(product_repo, codes)

            # Get nhanh_ids for products found in DB
            nhanh_ids = [p.nhanh_id for p in nhanh_by_code.values()]

            # Fetch inventory using codes (proxy will search by name)
            inventory, api_error = await _fetch_inventory(
                nhanh_service, nhanh_ids, product_codes=codes
            )

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
