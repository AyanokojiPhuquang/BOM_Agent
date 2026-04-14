"""Run datasheet matching against Nhanh products in the local DB.

Usage:
    uv run python scripts/match_datasheets.py                    # match unmatched, persist
    uv run python scripts/match_datasheets.py --dry-run          # preview only, no DB writes
    uv run python scripts/match_datasheets.py --limit 10         # only process first 10 products
    uv run python scripts/match_datasheets.py --rematch-all      # re-match all products
    uv run python scripts/match_datasheets.py --layer1-only      # skip LLM, code match only
"""

import argparse
import asyncio
import sys
from pathlib import Path

from loguru import logger
from sqlmodel import SQLModel

logger.remove()
logger.add(sys.stderr, level="INFO")

import src.configs  # noqa: E402, F401
import src.db.models.nhanh  # noqa: E402, F401

from src.configs import SETTINGS  # noqa: E402
from src.db.database import engine, get_manual_db_session  # noqa: E402
from src.db.repositories.nhanh import NhanhProductRepository  # noqa: E402
from src.services.nhanh.datasheet_matcher import DatasheetMatcher, MatchResult  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Match Nhanh products to datasheets")
    parser.add_argument("--dry-run", action="store_true", help="Preview matches without saving to DB")
    parser.add_argument("--limit", type=int, default=None, help="Max number of products to process")
    parser.add_argument("--rematch-all", action="store_true", help="Re-match all products, not just unmatched")
    parser.add_argument("--layer1-only", action="store_true", help="Only run exact code matching, skip LLM")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show debug logs")
    return parser.parse_args()


def print_results(results: list[MatchResult], dry_run: bool) -> None:
    matched = [r for r in results if r.datasheet_path]
    unmatched = [r for r in results if not r.datasheet_path]

    print(f"\n{'=' * 60}")
    print(f"  Total processed: {len(results)}")
    print(f"  Matched:         {len(matched)}")
    print(f"  Unmatched:       {len(unmatched)}")
    if dry_run:
        print("  Mode:            DRY RUN (no DB writes)")
    print(f"{'=' * 60}")

    if matched:
        print(f"\n--- Matched ({len(matched)}) ---")
        for r in matched:
            print(f"  [{r.match_layer}] ({r.confidence}) {r.product_name}")
            print(f"    -> {r.datasheet_path}")

    if unmatched:
        print(f"\n--- Unmatched ({len(unmatched)}) ---")
        for r in unmatched:
            print(f"  {r.product_name} (nhanh_id={r.nhanh_id})")


async def fetch_products(repo: NhanhProductRepository, rematch_all: bool, limit: int | None):
    products = (
        await repo.get_all_products()
        if rematch_all
        else await repo.get_unmatched_products()
    )
    if limit:
        products = products[:limit]
    return products


async def save_results(repo, session, results: list[MatchResult]) -> int:
    matches = [(r.nhanh_id, r.datasheet_path) for r in results if r.datasheet_path]
    if not matches:
        return 0
    updated = await repo.update_datasheet_paths(matches)
    await session.commit()
    return updated


async def ensure_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def main() -> None:
    args = parse_args()

    if args.verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")

    matcher = DatasheetMatcher(datasheets_dir=str(Path(SETTINGS.datasheets_dir).resolve()))

    await ensure_tables()

    async with get_manual_db_session() as session:
        repo = NhanhProductRepository(session)
        products = await fetch_products(repo, args.rematch_all, args.limit)

        if not products:
            print("No products to match.")
            return

        print(f"Processing {len(products)} products...")

        results = await matcher.match_products(products, code_match_only=args.layer1_only)

        print_results(results, dry_run=args.dry_run)

        if not args.dry_run:
            updated = await save_results(repo, session, results)
            print(f"\nSaved {updated} matches to DB.")


if __name__ == "__main__":
    asyncio.run(main())
