import json
from datetime import datetime, timezone
from pathlib import Path

from loguru import logger

from src.app.schemas.nhanh import (
    NhanhCategoryListResponse,
    NhanhCategorySearchRequest,
    NhanhInventoryRequest,
    NhanhInventoryResponse,
    NhanhProductDetailRequest,
    NhanhProductItem,
    NhanhProductListResponse,
    NhanhProductSearchRequest,
    NhanhTokenStatusResponse,
)
from src.configs import SETTINGS
from src.db.models.nhanh import NhanhToken
from src.db.repositories.nhanh import NhanhProductRepository, NhanhTokenRepository
from src.services.nhanh.client import NhanhClient
from src.services.nhanh.datasheet_matcher import DatasheetMatcher

class NhanhService:
    def __init__(self, repo: NhanhTokenRepository):
        self.repo = repo
        self._datasheet_matcher = DatasheetMatcher(
            datasheets_dir=str(Path(SETTINGS.datasheets_dir).resolve())
        )

    async def exchange_and_save_token(self, access_code: str) -> NhanhToken:
        """Exchange an OAuth access code and persist the resulting token."""
        data = await NhanhClient.exchange_access_code(access_code)

        token = NhanhToken(
            business_id=str(data["businessId"]),
            access_token=data["accessToken"],
            expired_at=data["expiredAt"],
            depot_ids=json.dumps(data.get("depotIds")) if data.get("depotIds") else None,
            page_ids=json.dumps(data.get("pageIds")) if data.get("pageIds") else None,
            permissions=json.dumps(data.get("permissions")) if data.get("permissions") else None,
        )
        await self.repo.save(token)
        await self.repo.session.commit()

        logger.info(f"Nhanh token saved for business {token.business_id}")
        return token

    async def get_token_status(self) -> NhanhTokenStatusResponse:
        """Return the current connection status."""
        token = await self.repo.get_latest()
        if not token:
            return NhanhTokenStatusResponse(connected=False, message="No Nhanh.vn token found")

        is_valid = token.expired_at > self._now_ts()
        return NhanhTokenStatusResponse(
            connected=is_valid,
            business_id=token.business_id,
            expired_at=token.expired_at,
            message="Token is valid" if is_valid else "Token has expired",
        )

    async def get_inventory(
        self, req: NhanhInventoryRequest | None = None,
    ) -> NhanhInventoryResponse:
        """Fetch remaining stock from Nhanh using a valid token."""
        client = await self._get_client()

        req = req or NhanhInventoryRequest()
        filters: dict = {}
        if req.product_ids:
            filters["ids"] = req.product_ids
        if req.category_ids:
            filters["categoryIds"] = req.category_ids
        if req.depot_ids:
            filters["depotIds"] = req.depot_ids

        paginator = {"size": req.page_size, "page": req.page}

        return await client.get_inventory(
            filters=filters or None,
            paginator=paginator,
        )

    async def search_products(
        self, req: NhanhProductSearchRequest | None = None,
    ) -> NhanhProductListResponse:
        """Search / list products from Nhanh."""
        client = await self._get_client()

        req = req or NhanhProductSearchRequest()
        filters: dict = {}
        if req.ids:
            filters["ids"] = req.ids
        if req.name:
            filters["name"] = req.name
        if req.barcode:
            filters["barcode"] = req.barcode
        if req.category_id is not None:
            filters["categoryId"] = req.category_id
        if req.brand_id is not None:
            filters["brandId"] = req.brand_id
        if req.price_from is not None:
            filters["priceFrom"] = req.price_from
        if req.price_to is not None:
            filters["priceTo"] = req.price_to
        if req.status is not None:
            filters["status"] = req.status
        if req.parent_id is not None:
            filters["parentId"] = req.parent_id
        if req.imei:
            filters["imei"] = req.imei

        paginator: dict = {"size": req.page_size, "page": req.page}
        if req.sort_by:
            paginator["sort"] = {req.sort_by: req.sort_order}

        return await client.get_products(
            filters=filters or None,
            paginator=paginator,
        )

    async def get_categories(
        self, req: NhanhCategorySearchRequest | None = None,
    ) -> NhanhCategoryListResponse:
        """Fetch product categories from Nhanh."""
        client = await self._get_client()

        req = req or NhanhCategorySearchRequest()
        filters: dict = {}
        if req.ids:
            filters["ids"] = req.ids
        if req.name:
            filters["name"] = req.name
        if req.code:
            filters["code"] = req.code
        if req.status is not None:
            filters["status"] = req.status

        paginator: dict = {"size": req.page_size}

        return await client.get_categories(
            filters=filters or None,
            paginator=paginator,
        )

    async def get_product_detail(
        self, req: NhanhProductDetailRequest,
    ) -> list[NhanhProductItem]:
        """Get detail for specific product IDs."""
        client = await self._get_client()
        return await client.get_product_detail(req.product_ids)

    async def sync_all_products(
        self,
        product_repo: NhanhProductRepository,
        force_full: bool = False,
        page_size: int = 100,
    ) -> dict:
        """Fetch products from Nhanh and upsert into local DB.

        If a previous sync exists and force_full is False, performs an
        incremental sync using updatedAtFrom/updatedAtTo filters.
        Note: updatedAt only covers product info changes (name, price, etc.),
        NOT inventory changes. Use webhooks for inventory updates.
        """
        client = await self._get_client()

        # Determine sync type based on last sync
        last_sync = await product_repo.get_last_sync()
        filters: dict = {}

        if last_sync and not force_full:
            sync_type = "incremental"
            updated_from = int(last_sync.started_at.timestamp())
            updated_to = int(datetime.now(timezone.utc).timestamp())
            filters["updatedAtFrom"] = updated_from
            filters["updatedAtTo"] = updated_to
            logger.info(f"Incremental sync: updatedAtFrom={updated_from}, updatedAtTo={updated_to}")
        else:
            sync_type = "full"
            logger.info("Full sync: fetching all products")

        sync_log = await product_repo.create_sync_log(sync_type)

        total_created = 0
        total_updated = 0
        pages_fetched = 0
        next_cursor_id: int | None = None

        while True:
            paginator: dict = {"size": page_size, "page": 1}
            if next_cursor_id is not None:
                paginator["next"] = {"id": next_cursor_id}

            response = await client.get_products(
                filters=filters or None,
                paginator=paginator,
            )
            pages_fetched += 1

            if response.items:
                created, updated = await product_repo.upsert_batch(response.items)
                total_created += created
                total_updated += updated

            logger.info(
                f"[{sync_type}] Synced page {pages_fetched}: {len(response.items)} items, "
                f"+{total_created} created, ~{total_updated} updated"
            )

            if not response.next_cursor_id or not response.items:
                break
            next_cursor_id = response.next_cursor_id

        await product_repo.finish_sync_log(
            sync_log, total_created, total_updated, pages_fetched
        )

        # Auto-match newly synced products to datasheets
        total_matched = 0
        total_unmatched = 0
        try:
            results = await self.match_datasheets(product_repo)
            total_matched = sum(1 for r in results if r.datasheet_path)
            total_unmatched = len(results) - total_matched
        except Exception as e:
            logger.warning(f"Datasheet matching after sync failed (non-fatal): {e}")

        return {
            "sync_type": sync_type,
            "total_created": total_created,
            "total_updated": total_updated,
            "total_pages_fetched": pages_fetched,
            "total_matched": total_matched,
            "total_unmatched": total_unmatched,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def match_datasheets(
        self,
        product_repo: NhanhProductRepository,
        rematch_all: bool = False,
    ) -> list:
        """Run datasheet matching and persist results.

        Returns list of MatchResult.
        """
        products = (
            await product_repo.get_all_products()
            if rematch_all
            else await product_repo.get_unmatched_products()
        )
        if not products:
            return []

        results = await self._datasheet_matcher.match_products(products)
        await self._persist_matches(product_repo, results)
        return results

    async def _persist_matches(
        self,
        product_repo: NhanhProductRepository,
        results: list,
    ) -> int:
        matches = [(r.nhanh_id, r.datasheet_path) for r in results if r.datasheet_path]
        if not matches:
            return 0
        updated = await product_repo.update_datasheet_paths(matches)
        logger.info(f"Persisted {updated} datasheet matches")
        return updated

    async def _get_client(self) -> NhanhClient:
        """Resolve a valid token and return a ready-to-use client."""
        token = await self.repo.get_latest()
        if not token:
            raise ValueError("No Nhanh.vn token found. Please connect first.")
        if token.expired_at <= self._now_ts():
            raise ValueError("Nhanh.vn token has expired. Please reconnect.")
        return NhanhClient(token.business_id, token.access_token)

    @staticmethod
    def _now_ts() -> int:
        return int(datetime.now(timezone.utc).timestamp())
