import httpx
from loguru import logger

from src.app.schemas.nhanh import (
    NhanhCategoryItem,
    NhanhCategoryListResponse,
    NhanhDepotInventory,
    NhanhInventoryItem,
    NhanhInventoryResponse,
    NhanhProductItem,
    NhanhProductListResponse,
)
from src.configs import SETTINGS


class NhanhApiError(Exception):
    """Raised when Nhanh API returns a non-success response."""

    def __init__(self, message: str, raw: dict | None = None):
        super().__init__(message)
        self.raw = raw


class NhanhClient:
    """HTTP client for Nhanh.vn API v3.0."""

    def __init__(self, business_id: str, access_token: str):
        self.base_url = SETTINGS.nhanh.api_base_url
        self.app_id = SETTINGS.nhanh.app_id
        self.business_id = business_id
        self.access_token = access_token

    async def _post(self, endpoint: str, data: dict | None = None) -> dict:
        url = f"{self.base_url}/v{SETTINGS.nhanh.api_version}/{endpoint}"
        params = {"appId": self.app_id, "businessId": self.business_id}
        headers = {
            "Authorization": self.access_token,
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=30) as client:
            logger.debug(f"Nhanh API POST {url}")
            resp = await client.post(url, params=params, headers=headers, json=data or {})
            resp.raise_for_status()
            result = resp.json()

        if result.get("code") != 1:
            raise NhanhApiError(
                result.get("messages", str(result)), raw=result
            )
        return result

    @staticmethod
    async def exchange_access_code(access_code: str) -> dict:
        """Exchange an OAuth access code for an access token.

        Returns the raw ``data`` dict from Nhanh on success.
        Raises ``NhanhApiError`` when the API reports failure.
        """
        url = (
            f"{SETTINGS.nhanh.api_base_url}/v{SETTINGS.nhanh.api_version}"
            f"/app/getaccesstoken"
        )
        params = {"appId": SETTINGS.nhanh.app_id}
        payload = {
            "accessCode": access_code,
            "secretKey": SETTINGS.nhanh.secret_key,
        }

        async with httpx.AsyncClient(timeout=30) as client:
            logger.info("Exchanging Nhanh access code for token")
            resp = await client.post(url, params=params, json=payload)
            resp.raise_for_status()
            result = resp.json()

        data = result.get("data", {})
        if not data or result.get("code") != 1:
            raise NhanhApiError(
                f"Token exchange failed: {result}", raw=result
            )
        return data

    async def get_inventory(
        self, filters: dict | None = None, paginator: dict | None = None
    ) -> NhanhInventoryResponse:
        """Fetch product inventory and parse into typed response."""
        data: dict = {}
        if filters:
            data["filters"] = filters
        if paginator:
            data["paginator"] = paginator

        result = await self._post("product/inventory", data)

        raw_data = result.get("data", {})
        products = raw_data.get("products", raw_data)

        items: list[NhanhInventoryItem] = []
        if isinstance(products, dict):
            for pid, info in products.items():
                inventory = info.get("inventory", info)
                depot_list = [
                    NhanhDepotInventory(
                        depot_id=int(d.get("depotId", 0)),
                        remain=int(d.get("remain", 0)),
                        available=int(d.get("available", 0)),
                    )
                    for d in inventory.get("depots", [])
                ]
                items.append(NhanhInventoryItem(
                    product_id=int(pid),
                    remain=int(inventory.get("remain", 0)),
                    shipping=int(inventory.get("shipping", 0)),
                    damaged=int(inventory.get("damaged", 0)),
                    holding=int(inventory.get("holding", 0)),
                    available=int(inventory.get("available", 0)),
                    warranty=int(inventory.get("warranty", 0)),
                    depots=depot_list,
                ))

        paginator_data = raw_data.get("paginator", {})
        return NhanhInventoryResponse(
            items=items,
            total_pages=int(paginator_data.get("totalPages", 0)),
            current_page=int(paginator_data.get("page", 1)),
        )

    async def get_products(
        self, filters: dict | None = None, paginator: dict | None = None
    ) -> NhanhProductListResponse:
        """Search / list products and parse into typed response."""
        data: dict = {}
        if filters:
            data["filters"] = filters
        if paginator:
            data["paginator"] = paginator

        result = await self._post("product/list", data)

        raw_items = result.get("data", [])
        items: list[NhanhProductItem] = []
        if isinstance(raw_items, list):
            for info in raw_items:
                inventory = info.get("inventory", {})
                prices = info.get("prices", {})
                items.append(NhanhProductItem(
                    id=int(info.get("id", 0)),
                    parent_id=info.get("parentId"),
                    name=str(info.get("name", "")),
                    code=str(info.get("code", "")),
                    barcode=str(info.get("barcode", "")),
                    price=float(prices.get("retail", 0)),
                    import_price=float(prices.get("import", 0)),
                    category_id=info.get("categoryId"),
                    brand_id=info.get("brandId"),
                    status=int(info.get("status", 0)),
                    remain=int(inventory.get("remain", 0)),
                    available=int(inventory.get("available", 0)),
                    image=str(info.get("image", "")),
                ))

        paginator_data = result.get("paginator", {})
        next_cursor = paginator_data.get("next", {})
        return NhanhProductListResponse(
            items=items,
            next_cursor_id=next_cursor.get("id"),
        )

    async def get_categories(
        self, filters: dict | None = None, paginator: dict | None = None
    ) -> NhanhCategoryListResponse:
        """Fetch product categories and parse into typed response."""
        data: dict = {}
        if filters:
            data["filters"] = filters
        if paginator:
            data["paginator"] = paginator

        result = await self._post("product/category", data)

        raw_items = result.get("data", [])
        items: list[NhanhCategoryItem] = []
        if isinstance(raw_items, list):
            for info in raw_items:
                items.append(NhanhCategoryItem(
                    id=int(info.get("id", 0)),
                    parent_id=info.get("parentId"),
                    code=str(info.get("code", "")),
                    name=str(info.get("name", "")),
                    order=int(info.get("order", 0)),
                    image=str(info.get("image", "")),
                    content=str(info.get("content", "")),
                    status=int(info.get("status", 0)),
                ))

        paginator_data = result.get("paginator", {})
        return NhanhCategoryListResponse(
            items=items,
            next_cursor=paginator_data.get("next"),
        )

    async def get_product_detail(self, product_ids: list[int]) -> list[NhanhProductItem]:
        """Fetch detail for specific product IDs."""
        result = await self._post("product/detail", {"ids": product_ids})

        raw_data = result.get("data", {})
        products = raw_data.get("products", raw_data)

        items: list[NhanhProductItem] = []
        if isinstance(products, dict):
            for pid, info in products.items():
                inventory = info.get("inventory", {})
                items.append(NhanhProductItem(
                    id=int(pid),
                    name=str(info.get("name", "")),
                    code=str(info.get("code", "")),
                    barcode=str(info.get("barcode", "")),
                    price=float(info.get("price", 0)),
                    category_id=info.get("categoryId"),
                    brand_id=info.get("brandId"),
                    remain=int(inventory.get("remain", 0)),
                    available=int(inventory.get("available", 0)),
                    image=str(info.get("image", "")),
                ))
        return items

    @staticmethod
    async def check_access_token(business_id: str, access_token: str) -> dict:
        """Check if a stored access token is still valid."""
        url = (
            f"{SETTINGS.nhanh.api_base_url}/v{SETTINGS.nhanh.api_version}"
            f"/app/checkaccesstoken"
        )
        params = {
            "appId": SETTINGS.nhanh.app_id,
            "businessId": business_id,
        }
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json",
        }
        payload = {"secretKey": SETTINGS.nhanh.secret_key}

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, params=params, headers=headers, json=payload)
            resp.raise_for_status()
            return resp.json()
