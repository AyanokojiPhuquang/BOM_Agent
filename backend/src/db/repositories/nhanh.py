from datetime import datetime, timezone

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.nhanh import NhanhProductItem
from src.db.models.nhanh import NhanhProduct, NhanhSyncLog, NhanhToken


# --- Standalone functions ---


async def save_token(session: AsyncSession, token: NhanhToken) -> NhanhToken:
    session.add(token)
    await session.flush()
    return token


async def get_latest_token(session: AsyncSession) -> NhanhToken | None:
    stmt = select(NhanhToken).order_by(NhanhToken.created_at.desc()).limit(1)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_token_by_business_id(
    session: AsyncSession, business_id: str
) -> NhanhToken | None:
    stmt = (
        select(NhanhToken)
        .where(NhanhToken.business_id == business_id)
        .order_by(NhanhToken.created_at.desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def delete_tokens_by_business_id(
    session: AsyncSession, business_id: str
) -> int:
    result = await session.execute(
        delete(NhanhToken).where(NhanhToken.business_id == business_id)
    )
    return result.rowcount


# --- Class wrapper ---


class NhanhTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, token: NhanhToken) -> NhanhToken:
        return await save_token(self.session, token)

    async def get_latest(self) -> NhanhToken | None:
        return await get_latest_token(self.session)

    async def get_by_business_id(self, business_id: str) -> NhanhToken | None:
        return await get_token_by_business_id(self.session, business_id)

    async def delete_by_business_id(self, business_id: str) -> int:
        return await delete_tokens_by_business_id(self.session, business_id)


# --- Product functions ---


async def upsert_products(
    session: AsyncSession,
    items: list[NhanhProductItem],
) -> tuple[int, int]:
    """Upsert a batch of products. Returns (created_count, updated_count)."""
    created = 0
    updated = 0
    now = datetime.now(timezone.utc)

    nhanh_ids = [item.id for item in items]
    stmt = select(NhanhProduct).where(NhanhProduct.nhanh_id.in_(nhanh_ids))
    result = await session.execute(stmt)
    existing_map = {p.nhanh_id: p for p in result.scalars().all()}

    for item in items:
        existing = existing_map.get(item.id)
        if existing:
            existing.parent_id = item.parent_id
            existing.name = item.name
            existing.code = item.code
            existing.barcode = item.barcode
            existing.price = item.price
            existing.import_price = item.import_price
            existing.category_id = item.category_id
            existing.brand_id = item.brand_id
            existing.status = item.status
            existing.remain = item.remain
            existing.available = item.available
            existing.image = item.image
            existing.updated_at = now
            existing.last_synced_at = now
            session.add(existing)
            updated += 1
        else:
            product = NhanhProduct(
                nhanh_id=item.id,
                parent_id=item.parent_id,
                name=item.name,
                code=item.code,
                barcode=item.barcode,
                price=item.price,
                import_price=item.import_price,
                category_id=item.category_id,
                brand_id=item.brand_id,
                status=item.status,
                remain=item.remain,
                available=item.available,
                image=item.image,
                created_at=now,
                updated_at=now,
                last_synced_at=now,
            )
            session.add(product)
            created += 1

    await session.flush()
    return created, updated


class NhanhProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_batch(self, items: list[NhanhProductItem]) -> tuple[int, int]:
        return await upsert_products(self.session, items)

    async def get_last_sync(self) -> NhanhSyncLog | None:
        stmt = (
            select(NhanhSyncLog)
            .where(NhanhSyncLog.finished_at.is_not(None))
            .order_by(NhanhSyncLog.finished_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_sync_log(self, sync_type: str) -> NhanhSyncLog:
        log = NhanhSyncLog(sync_type=sync_type)
        self.session.add(log)
        await self.session.flush()
        return log

    async def finish_sync_log(
        self, log: NhanhSyncLog, created: int, updated: int, pages: int
    ) -> NhanhSyncLog:
        log.total_created = created
        log.total_updated = updated
        log.total_pages_fetched = pages
        log.finished_at = datetime.now(timezone.utc)
        self.session.add(log)
        await self.session.flush()
        return log

    async def get_by_datasheet_paths(self, paths: list[str]) -> list[NhanhProduct]:
        """Find NhanhProducts by their datasheet_path field."""
        stmt = select(NhanhProduct).where(NhanhProduct.datasheet_path.in_(paths))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_codes(self, codes: list[str]) -> list[NhanhProduct]:
        """Find NhanhProducts by their code field (case-insensitive)."""
        normalized = [c.strip().upper() for c in codes]
        stmt = select(NhanhProduct).where(func.upper(NhanhProduct.code).in_(normalized))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_all_products(self) -> list[NhanhProduct]:
        """Get all synced products."""
        stmt = select(NhanhProduct)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_unmatched_products(self) -> list[NhanhProduct]:
        """Get products that don't have a datasheet_path assigned."""
        stmt = select(NhanhProduct).where(NhanhProduct.datasheet_path.is_(None))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_datasheet_paths(
        self, matches: list[tuple[int, str | None]]
    ) -> int:
        """Update datasheet_path for a list of (nhanh_id, datasheet_path) pairs.

        Returns the number of products updated.
        """
        updated = 0
        nhanh_ids = [nid for nid, _ in matches]
        stmt = select(NhanhProduct).where(NhanhProduct.nhanh_id.in_(nhanh_ids))
        result = await self.session.execute(stmt)
        product_map = {p.nhanh_id: p for p in result.scalars().all()}

        for nhanh_id, datasheet_path in matches:
            product = product_map.get(nhanh_id)
            if product and datasheet_path:
                product.datasheet_path = datasheet_path
                product.updated_at = datetime.now(timezone.utc)
                self.session.add(product)
                updated += 1

        await self.session.flush()
        return updated

    async def get_match_status(self) -> dict:
        """Get counts of matched vs unmatched products."""

        total_stmt = select(func.count()).select_from(NhanhProduct)
        total_result = await self.session.execute(total_stmt)
        total = total_result.scalar() or 0

        matched_stmt = (
            select(func.count())
            .select_from(NhanhProduct)
            .where(NhanhProduct.datasheet_path.is_not(None))
        )
        matched_result = await self.session.execute(matched_stmt)
        matched = matched_result.scalar() or 0

        return {
            "total_products": total,
            "matched": matched,
            "unmatched": total - matched,
            "match_rate": matched / total if total > 0 else 0.0,
        }
