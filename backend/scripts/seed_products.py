"""Seed nhanh_products from local datasheets.

Scans the datasheets directory and inserts a NhanhProduct row for each .md file,
using the folder name as the product code and a generated nhanh_id.
This allows generate_bom and check_product_inventory to resolve product codes
without requiring a live Nhanh.vn OAuth connection.

Usage (inside container):
    uv run python -m scripts.seed_products
"""

import asyncio
import os
import random
from pathlib import Path

from src.configs import SETTINGS
from src.db.database import get_manual_db_session
from src.db.models.nhanh import NhanhProduct
from src.db.repositories.nhanh import NhanhProductRepository


def discover_products(datasheets_dir: str) -> list[dict]:
    """Walk the datasheets directory and extract product info from .md files."""
    products = []
    root = Path(datasheets_dir).resolve()

    for md_file in root.rglob("*.md"):
        # Product code = parent folder name (e.g. SFP-10G-LR)
        code = md_file.parent.name.strip()
        if not code:
            continue

        # Datasheet path relative to datasheets root
        rel_path = str(md_file.relative_to(root))

        # Derive a readable name
        name = f"ModuleTek {code}"

        products.append({
            "code": code,
            "name": name,
            "datasheet_path": rel_path,
        })

    return products


async def seed():
    datasheets_dir = str(Path(SETTINGS.datasheets_dir).resolve())
    products = discover_products(datasheets_dir)

    if not products:
        print(f"No datasheets found in {datasheets_dir}")
        return

    print(f"Found {len(products)} products from datasheets")

    async with get_manual_db_session() as session:
        repo = NhanhProductRepository(session)

        created = 0
        skipped = 0
        for i, p in enumerate(products):
            # Check if already exists by code
            existing = await repo.get_by_codes([p["code"]])
            if existing:
                skipped += 1
                continue

            product = NhanhProduct(
                nhanh_id=90000 + i,  # Fake nhanh_id
                name=p["name"],
                code=p["code"],
                datasheet_path=p["datasheet_path"],
                price=0,
                import_price=0,
                status=1,
                remain=random.randint(10, 200),  # Fake stock for testing
                available=random.randint(5, 150),
            )
            session.add(product)
            created += 1

        await session.commit()
        print(f"Seeded {created} products, skipped {skipped} (already exist)")


if __name__ == "__main__":
    asyncio.run(seed())
