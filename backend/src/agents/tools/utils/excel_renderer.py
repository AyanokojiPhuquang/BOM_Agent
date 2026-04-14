"""Excel renderer for BOM output.

Converts a GenerateBomOutput into a styled .xlsx workbook.
"""

from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from src.agents.tools.schemas import GenerateBomOutput, ProductInventoryStatus, STATUS_LABELS

# Styling constants
_HEADER_FONT = Font(name="Calibri", bold=True, size=11, color="FFFFFF")
_HEADER_FILL = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
_HEADER_ALIGNMENT = Alignment(horizontal="center", vertical="center", wrap_text=True)
_TITLE_FONT = Font(name="Calibri", bold=True, size=14, color="2F5496")
_SUBTITLE_FONT = Font(name="Calibri", size=10, color="666666")
_CELL_BORDER = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9"),
)
_ALT_ROW_FILL = PatternFill(start_color="F2F7FC", end_color="F2F7FC", fill_type="solid")

_IN_STOCK_FILL = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
_PARTIAL_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
_OUT_OF_STOCK_FILL = PatternFill(start_color="FCE4EC", end_color="FCE4EC", fill_type="solid")

_STATUS_FILLS = {
    "in_stock": _IN_STOCK_FILL,
    "partial": _PARTIAL_FILL,
    "out_of_stock": _OUT_OF_STOCK_FILL,
}

# BOM sheet columns
_BOM_COLUMNS = [
    ("#", 5),
    ("SKU", 22),
    ("Brand", 12),
    ("Description", 35),
    ("Vendor", 14),
    ("Data Rate", 10),
    ("Fiber", 13),
    ("Wavelength", 12),
    ("Distance", 10),
    ("Connector", 10),
    ("Qty", 6),
    ("Unit Price", 12),
    ("Notes", 30),
]

_INV_COLUMNS = [
    ("Requested", 10),
    ("Available", 10),
    ("In Stock", 10),
    ("Status", 16),
]


def _resolve_columns(has_inventory: bool) -> list[tuple[str, int]]:
    """Return the full column list based on whether inventory data is present."""
    columns = list(_BOM_COLUMNS)
    if has_inventory:
        columns.extend(_INV_COLUMNS)
    return columns


def _write_title_rows(ws: Worksheet, bom: GenerateBomOutput, last_col: str) -> None:
    """Write the title and subtitle rows."""
    ws.merge_cells(f"A1:{last_col}1")
    title_cell = ws["A1"]
    title_cell.value = f"BOM — {bom.customer_name}"
    title_cell.font = _TITLE_FONT
    title_cell.alignment = Alignment(vertical="center")
    ws.row_dimensions[1].height = 30

    subtitle_parts = ["Starlinks"]
    if bom.customer_phone:
        subtitle_parts.append(f"SĐT: {bom.customer_phone}")
    subtitle_parts.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    ws.merge_cells(f"A2:{last_col}2")
    subtitle_cell = ws["A2"]
    subtitle_cell.value = " | ".join(subtitle_parts)
    subtitle_cell.font = _SUBTITLE_FONT


def _write_header_row(ws: Worksheet, columns: list[tuple[str, int]], row: int) -> None:
    """Write the styled header row."""
    for col_idx, (col_name, col_width) in enumerate(columns, start=1):
        cell = ws.cell(row=row, column=col_idx, value=col_name)
        cell.font = _HEADER_FONT
        cell.fill = _HEADER_FILL
        cell.alignment = _HEADER_ALIGNMENT
        cell.border = _CELL_BORDER
        ws.column_dimensions[get_column_letter(col_idx)].width = col_width


def _line_item_values(item) -> list:
    """Extract cell values from a BomLineItem."""
    return [
        item.line,
        item.sku,
        item.brand,
        item.description,
        item.vendor_compatibility,
        item.data_rate,
        item.fiber_type,
        item.wavelength or "",
        item.max_distance,
        item.connector,
        item.quantity,
        f"${item.unit_price_usd:.2f}" if item.unit_price_usd else "",
        item.notes or "",
    ]


def _inventory_values(inv: ProductInventoryStatus | None) -> list:
    """Extract cell values from a ProductInventoryStatus."""
    if not inv:
        return ["", "", "", ""]
    return [
        inv.quantity_requested,
        inv.available,
        inv.remain,
        STATUS_LABELS.get(inv.status_label, inv.status_label),
    ]


def _write_data_rows(
    ws: Worksheet,
    bom: GenerateBomOutput,
    header_row: int,
    total_cols: int,
    inventory_statuses: list[ProductInventoryStatus] | None,
) -> None:
    """Write BOM line item rows with optional inventory columns."""
    has_inventory = bool(inventory_statuses)

    for row_idx, item in enumerate(bom.line_items, start=header_row + 1):
        values = _line_item_values(item)

        if has_inventory:
            item_idx = row_idx - header_row - 1
            inv = inventory_statuses[item_idx] if item_idx < len(inventory_statuses) else None
            values.extend(_inventory_values(inv))

        for col_idx, value in enumerate(values, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = _CELL_BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if (row_idx - header_row) % 2 == 0:
                cell.fill = _ALT_ROW_FILL

        # Color-code inventory status cell
        if has_inventory and item_idx < len(inventory_statuses):
            inv = inventory_statuses[item_idx]
            fill = _STATUS_FILLS.get(inv.status_label)
            if fill:
                ws.cell(row=row_idx, column=total_cols).fill = fill


def _write_assumptions(
    ws: Worksheet,
    assumptions: list[str],
    start_row: int,
    last_col: str,
) -> None:
    """Write the assumptions section below the data rows."""
    ws.merge_cells(f"A{start_row}:{last_col}{start_row}")
    header = ws.cell(row=start_row, column=1, value="Assumptions")
    header.font = Font(name="Calibri", bold=True, size=11, color="2F5496")

    for i, assumption in enumerate(assumptions):
        row = start_row + 1 + i
        ws.merge_cells(f"A{row}:{last_col}{row}")
        ws.cell(row=row, column=1, value=f"• {assumption}")


def render_bom_excel(
    bom: GenerateBomOutput,
    output_dir: Path,
    inventory_statuses: list[ProductInventoryStatus] | None = None,
) -> Path:
    """Render a BOM to an Excel workbook.

    Args:
        bom: The structured BOM output from the subagent.
        output_dir: Directory to save the file in.
        inventory_statuses: Optional real-time inventory data per product.

    Returns:
        Path to the generated .xlsx file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = bom.customer_name.lower().replace(" ", "_")[:30]
    filepath = output_dir / f"{timestamp}_{slug}.xlsx"

    has_inventory = bool(inventory_statuses)
    columns = _resolve_columns(has_inventory)
    total_cols = len(columns)
    last_col = get_column_letter(total_cols)

    wb = Workbook()
    ws = wb.active
    ws.title = "BOM"

    header_row = 4

    _write_title_rows(ws, bom, last_col)
    _write_header_row(ws, columns, header_row)
    _write_data_rows(ws, bom, header_row, total_cols, inventory_statuses)

    if bom.assumptions:
        assumptions_start = header_row + len(bom.line_items) + 2
        _write_assumptions(ws, bom.assumptions, assumptions_start, last_col)

    wb.save(filepath)
    return filepath
