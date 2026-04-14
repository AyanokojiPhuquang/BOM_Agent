"""Test script for inventory checking and BOM generation tools.

Tests each component individually, then runs the full generate_bom flow
using real products from the DB that have matching datasheet files.
"""

import asyncio
from pathlib import Path

from src.agents.tools.inventory_checker import (
    _build_status,
    _fetch_inventory,
    _find_nhanh_products,
    _normalize_path,
    check_inventory,
)
from src.agents.tools.schemas import BomProductItem, GenerateBomOutput, BomLineItem, ProductInventoryStatus
from src.agents.tools.excel_renderer import render_bom_excel
from src.agents.tools.generate_bom import (
    _format_bom_summary,
    _format_inventory_status,
    _build_tool_response,
    _read_all_product_files,
)
from src.db.database import get_manual_db_session
from src.db.repositories.nhanh import NhanhProductRepository, NhanhTokenRepository
from src.services.nhanh.service import NhanhService


# Use real products that exist in both DB and filesystem
TEST_ITEMS = [
    BomProductItem(
        product_filepath="/SFP/SFP-25G-CSR/SFP-25G-CSR.md",
        quantity=10,
        vendor="Cisco",
    ),
    BomProductItem(
        product_filepath="/QSFP/QSFP-100G-SWDM4/QSFP-100G-SWDM4.md",
        quantity=5,
        vendor="Juniper",
    ),
]


def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


async def test_normalize_path():
    separator("Test: _normalize_path")
    assert _normalize_path("/SFP/SFP-10G-LR/SFP-10G-LR.md") == "SFP/SFP-10G-LR/SFP-10G-LR.md"
    assert _normalize_path("SFP/SFP-10G-LR/SFP-10G-LR.md") == "SFP/SFP-10G-LR/SFP-10G-LR.md"
    print("PASS: normalize_path works correctly")


async def test_find_nhanh_products():
    separator("Test: _find_nhanh_products")
    async with get_manual_db_session() as session:
        repo = NhanhProductRepository(session)
        result = await _find_nhanh_products(
            repo,
            ["/SFP/SFP-25G-CSR/SFP-25G-CSR.md", "/QSFP/QSFP-100G-SWDM4/QSFP-100G-SWDM4.md"],
        )
        print(f"Found {len(result)} NhanhProducts:")
        for path, product in result.items():
            print(f"  path={path} -> nhanh_id={product.nhanh_id}, name={product.name}")

        assert len(result) > 0, "Should find at least one product"
        print("PASS")


async def test_fetch_inventory():
    separator("Test: _fetch_inventory")
    async with get_manual_db_session() as session:
        token_repo = NhanhTokenRepository(session)
        nhanh_service = NhanhService(token_repo)

        # Use known nhanh_ids
        nhanh_ids = [40759180, 40759193]  # SFP-25G-CSR, QSFP-100G-SWDM4
        result = await _fetch_inventory(nhanh_service, nhanh_ids)
        print(f"Inventory for {len(nhanh_ids)} products:")
        for pid, (available, remain) in result.items():
            print(f"  nhanh_id={pid}: available={available}, remain={remain}")
        print("PASS")


async def test_check_inventory():
    separator("Test: check_inventory (full flow)")
    statuses = await check_inventory(TEST_ITEMS)
    print(f"Got {len(statuses)} inventory statuses:")
    for s in statuses:
        print(f"  {s.product_filepath}: status={s.status_label}, "
              f"requested={s.quantity_requested}, available={s.available}, "
              f"remain={s.remain}, sufficient={s.is_sufficient}, "
              f"nhanh_name={s.nhanh_product_name}")

    assert len(statuses) == len(TEST_ITEMS), "Should have one status per item"

    # All statuses should have the nhanh product name (found in DB)
    for s in statuses:
        assert s.nhanh_product_name is not None, f"Should find NhanhProduct for {s.product_filepath}"
        assert s.nhanh_id is not None, f"Should have nhanh_id for {s.product_filepath}"
        # status_label depends on API availability:
        # - "in_stock"/"partial"/"out_of_stock" if API works
        # - "unavailable" if API auth fails (acceptable)
        assert s.status_label in ("in_stock", "partial", "out_of_stock", "unavailable"), \
            f"Unexpected status '{s.status_label}' for {s.product_filepath}"
    print("PASS")


async def test_check_inventory_not_found():
    separator("Test: check_inventory (product not in Nhanh)")
    fake_items = [
        BomProductItem(
            product_filepath="/SFP/FAKE-PRODUCT/FAKE-PRODUCT.md",
            quantity=1,
            vendor="Cisco",
        ),
    ]
    statuses = await check_inventory(fake_items)
    print(f"Got {len(statuses)} statuses:")
    for s in statuses:
        print(f"  {s.product_filepath}: status={s.status_label}")

    assert statuses[0].status_label == "not_found"
    print("PASS")


async def test_read_product_files():
    separator("Test: _read_all_product_files")
    results = await _read_all_product_files(TEST_ITEMS)
    print(f"Read {len(results)} product files:")
    for r in results:
        content_len = len(r["product_content"]) if r["product_content"] else 0
        print(f"  {r['product_filepath']}: content={content_len} chars, error={r['error']}")

    assert all(r["product_content"] for r in results), "All files should be readable"
    print("PASS")


async def test_format_inventory_status():
    separator("Test: _format_inventory_status")
    statuses = [
        ProductInventoryStatus(
            product_filepath="/SFP/SFP-25G-CSR/SFP-25G-CSR.md",
            nhanh_product_name="25GBASE-SR SFP",
            nhanh_id=1,
            quantity_requested=10,
            available=15,
            remain=20,
            is_sufficient=True,
            status_label="in_stock",
        ),
        ProductInventoryStatus(
            product_filepath="/QSFP/QSFP-100G-SWDM4/QSFP-100G-SWDM4.md",
            nhanh_product_name="100G QSFP28 SWDM4",
            nhanh_id=2,
            quantity_requested=5,
            available=2,
            remain=3,
            is_sufficient=False,
            status_label="partial",
        ),
        ProductInventoryStatus(
            product_filepath="/SFP/SFP-10G-LR/SFP-10G-LR.md",
            quantity_requested=3,
            status_label="not_found",
        ),
    ]
    output = _format_inventory_status(statuses)
    print(output)
    assert "Inventory Status" in output
    assert "In Stock" in output
    assert "Partial (need 5, have 2)" in output
    print("\nPASS")


async def test_excel_with_inventory():
    separator("Test: render_bom_excel with inventory")
    bom = GenerateBomOutput(
        is_valid=True,
        project_name="Test Project",
        customer_name="Test Customer",
        line_items=[
            BomLineItem(
                line=1, sku="SFP-25G-CSR", brand="ModuleTek",
                description="25G SFP28 SR", vendor_compatibility="Cisco",
                data_rate="25G", fiber_type="multi-mode", wavelength="850nm",
                max_distance="300m", connector="LC", quantity=10,
            ),
            BomLineItem(
                line=2, sku="QSFP-100G-SWDM4", brand="ModuleTek",
                description="100G QSFP28 SWDM4", vendor_compatibility="Juniper",
                data_rate="100G", fiber_type="multi-mode", wavelength="850-930nm",
                max_distance="150m", connector="LC", quantity=5,
            ),
        ],
        assumptions=["Vendor coding applied at order time"],
        summary="2 line items, 15 total units",
    )
    inv_statuses = [
        ProductInventoryStatus(
            product_filepath="/SFP/SFP-25G-CSR/SFP-25G-CSR.md",
            nhanh_product_name="25GBASE-SR SFP",
            nhanh_id=1,
            quantity_requested=10,
            available=15,
            remain=20,
            is_sufficient=True,
            status_label="in_stock",
        ),
        ProductInventoryStatus(
            product_filepath="/QSFP/QSFP-100G-SWDM4/QSFP-100G-SWDM4.md",
            nhanh_product_name="100G QSFP28 SWDM4",
            nhanh_id=2,
            quantity_requested=5,
            available=0,
            remain=0,
            is_sufficient=False,
            status_label="out_of_stock",
        ),
    ]

    output_dir = Path("data/generated_boms")
    filepath = render_bom_excel(bom, output_dir, inventory_statuses=inv_statuses)
    print(f"Excel generated: {filepath}")
    assert filepath.exists()
    assert filepath.suffix == ".xlsx"
    print(f"File size: {filepath.stat().st_size} bytes")
    print("PASS")


async def test_build_tool_response():
    separator("Test: _build_tool_response")
    bom = GenerateBomOutput(
        is_valid=True,
        project_name="Test Project",
        line_items=[
            BomLineItem(
                line=1, sku="SFP-25G-CSR", brand="ModuleTek",
                description="25G SFP28 SR", vendor_compatibility="Cisco",
                data_rate="25G", fiber_type="multi-mode",
                max_distance="300m", connector="LC", quantity=10,
            ),
        ],
        assumptions=[],
        summary="1 line item",
    )
    inv_statuses = [
        ProductInventoryStatus(
            product_filepath="/SFP/SFP-25G-CSR/SFP-25G-CSR.md",
            nhanh_product_name="25GBASE-SR SFP",
            nhanh_id=1,
            quantity_requested=10,
            available=15,
            remain=20,
            is_sufficient=True,
            status_label="in_stock",
        ),
    ]
    response = _build_tool_response(bom, inv_statuses, True)
    print(response)
    assert "BOM Generated Successfully" in response
    assert "Download BOM" not in response
    assert "Inventory Status" in response
    assert "Internal email sent" in response
    print("\nPASS")


async def main():
    print("\n" + "="*60)
    print("  STARLINKS BOM TOOL TESTS")
    print("="*60)

    tests = [
        test_normalize_path,
        test_find_nhanh_products,
        test_fetch_inventory,
        test_check_inventory,
        test_check_inventory_not_found,
        test_read_product_files,
        test_format_inventory_status,
        test_excel_with_inventory,
        test_build_tool_response,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            await test()
            passed += 1
        except Exception as e:
            print(f"FAIL: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    separator("RESULTS")
    print(f"  Passed: {passed}/{passed + failed}")
    if failed:
        print(f"  Failed: {failed}")
    else:
        print("  All tests passed!")


if __name__ == "__main__":
    asyncio.run(main())
