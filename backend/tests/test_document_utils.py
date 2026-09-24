"""Tests for PDF text-quality detection in document_utils.

These guard the decision to route a scanned/garbled PDF to vision/OCR instead
of feeding a broken text layer to the agent.
"""

from src.app.utils.document_utils import (
    _is_usable_pdf_text,
    _looks_like_garbled_text,
)


def _garbled_like_tender(num_lines: int = 60) -> str:
    # Mimic a broken OCR layer: mostly 1-2 char fragments.
    frags = ["n", "v", "e.", "o", "m", "@", "6", "1", "0", "bif"]
    return "\n".join(frags[i % len(frags)] for i in range(num_lines))


def _clean_tender_text() -> str:
    return (
        "PHẠM VI CUNG CẤP HÀNG HÓA\n"
        "| STT | Danh mục hàng hóa | Đơn vị | Khối lượng |\n"
        "| 1 | Module QSFP+ 40GE 10Km | Chiếc | 47 |\n"
        "| 2 | Module QSFP+ 40GE 40Km | Chiếc | 5 |\n"
        "| 3 | Module QSFP+ 100GE 10Km | Chiếc | 18 |\n"
        "| 4 | Module QSFP+ 100GE 40Km | Chiếc | 2 |\n"
        "| 5 | Module SFP+ 10GE 120km | Chiếc | 2 |\n"
    )


def test_garbled_text_is_detected():
    text = _garbled_like_tender()
    assert _looks_like_garbled_text(text) is True
    assert _is_usable_pdf_text(text) is False


def test_clean_text_is_usable():
    text = _clean_tender_text()
    assert _looks_like_garbled_text(text) is False
    assert _is_usable_pdf_text(text) is True


def test_short_document_is_not_flagged_as_garbled():
    # Too few lines to judge — don't false-positive tiny valid docs.
    text = "Báo giá\n| 1 | SFP-10G-LR | 10 |"
    assert _looks_like_garbled_text(text) is False


def test_sparse_text_is_not_usable():
    assert _is_usable_pdf_text("") is False
    assert _is_usable_pdf_text("short") is False
