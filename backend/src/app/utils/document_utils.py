"""Utility to extract text content from uploaded PDF and Excel files in chat.

Handles base64 data URL encoded files attached via the chat input.
Supports: .pdf (via pdfplumber, with LLM vision fallback for scanned PDFs),
           .xlsx/.xls (via openpyxl).
"""

import base64
import io

from loguru import logger

# Minimum chars per page to consider text extraction successful
MIN_CHARS_PER_PAGE = 50
# Max pages to send as images to LLM vision (cost control)
MAX_VISION_PAGES = 8


def extract_document_content(images: list) -> str:
    """Extract text from PDF/Excel attachments.

    For PDFs: tries pdfplumber first. If text is too sparse (scanned PDF),
    falls back to converting pages to images for LLM vision processing.

    Args:
        images: List of ImageAttachment-like objects with dataUrl and name fields.

    Returns:
        Combined text content from all document files, or empty string if none found.
    """
    contents: list[str] = []

    for attachment in images:
        name = attachment.name if hasattr(attachment, "name") else attachment.get("name", "")
        data_url = attachment.dataUrl if hasattr(attachment, "dataUrl") else attachment.get("dataUrl", "")

        if not data_url or "," not in data_url:
            continue

        lower_name = name.lower()

        if lower_name.endswith(".pdf"):
            result = _extract_pdf_smart(data_url, name)
            if result:
                contents.append(f"## File: {name}\n{result}")
        elif lower_name.endswith((".xlsx", ".xls")):
            text = _extract_excel(data_url, name)
            if text:
                contents.append(f"## File: {name}\n{text}")

    return "\n\n".join(contents)


def extract_pdf_as_images(images: list) -> list[str]:
    """For scanned PDFs, return base64 image URLs of pages for LLM vision.

    Returns list of base64 data URLs (image/png) that can be sent to LLM as image_urls.
    Only returns images for PDFs that don't have extractable text.
    """
    image_urls: list[str] = []

    for attachment in images:
        name = attachment.name if hasattr(attachment, "name") else attachment.get("name", "")
        data_url = attachment.dataUrl if hasattr(attachment, "dataUrl") else attachment.get("dataUrl", "")

        if not data_url or "," not in data_url:
            continue

        if not name.lower().endswith(".pdf"):
            continue

        # Check if this is a scanned PDF
        _, b64_data = data_url.split(",", 1)
        pdf_bytes = base64.b64decode(b64_data)

        if _is_scanned_pdf(pdf_bytes):
            page_images = _pdf_pages_to_images(pdf_bytes)
            image_urls.extend(page_images)

    return image_urls


def _extract_pdf_smart(data_url: str, filename: str) -> str:
    """Smart PDF extraction: text first, vision fallback for scans.

    Returns extracted text, or a marker indicating pages were sent as images.
    """
    _, b64_data = data_url.split(",", 1)
    pdf_bytes = base64.b64decode(b64_data)

    # Try text extraction first
    text = _extract_pdf_text(pdf_bytes)

    if text and len(text) > MIN_CHARS_PER_PAGE:
        # Good text extraction — use it
        if len(text) > 15000:
            text = text[:15000] + "\n\n[... truncated ...]"
        logger.info(f"PDF text extraction successful for {filename}: {len(text)} chars")
        return text

    # Text extraction failed or too sparse — this is likely a scanned PDF
    # Convert to images and return a note (images will be sent separately via image_urls)
    logger.info(f"PDF {filename} appears to be scanned (text too sparse). Will use vision.")
    return "[This PDF appears to be scanned/image-based. The page images have been sent for visual analysis.]"


def _is_scanned_pdf(pdf_bytes: bytes) -> bool:
    """Check if a PDF is scanned (no extractable text)."""
    text = _extract_pdf_text(pdf_bytes)
    return not text or len(text) < MIN_CHARS_PER_PAGE


def _extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes using pdfplumber."""
    try:
        import pdfplumber

        text_parts: list[str] = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

        return "\n".join(text_parts)
    except Exception as e:
        logger.error(f"pdfplumber extraction failed: {e}")
        return ""


def _pdf_pages_to_images(pdf_bytes: bytes, max_pages: int = MAX_VISION_PAGES) -> list[str]:
    """Convert PDF pages to base64 JPEG data URLs for LLM vision.

    Uses PyMuPDF (fitz) to render pages as compressed JPEG images.
    Resolution and quality are tuned to keep each image under ~200KB base64
    so the total payload stays within API limits.

    Args:
        pdf_bytes: Raw PDF file bytes.
        max_pages: Maximum number of pages to convert.

    Returns:
        List of base64 data URLs (data:image/jpeg;base64,...).
    """
    try:
        try:
            import fitz
        except ImportError:
            import pymupdf as fitz

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        image_urls: list[str] = []

        # Target: each image < 250KB base64 (~185KB raw JPEG)
        # Use 100 DPI for scanned docs (still readable for LLM vision)
        TARGET_DPI = 100
        JPEG_QUALITY = 60
        MAX_IMAGE_BYTES = 250_000  # max base64 size per image

        for i, page in enumerate(doc):
            if i >= max_pages:
                break

            # Render page at target DPI
            scale = TARGET_DPI / 72
            mat = fitz.Matrix(scale, scale)
            pix = page.get_pixmap(matrix=mat)

            # Convert to JPEG (much smaller than PNG for scanned content)
            jpeg_bytes = pix.tobytes("jpeg", jpg_quality=JPEG_QUALITY)

            # If still too large, reduce quality further
            if len(jpeg_bytes) > MAX_IMAGE_BYTES * 3 // 4:
                # Try lower DPI
                scale_low = 72 / 72  # 72 DPI
                mat_low = fitz.Matrix(scale_low, scale_low)
                pix_low = page.get_pixmap(matrix=mat_low)
                jpeg_bytes = pix_low.tobytes("jpeg", jpg_quality=50)

            b64 = base64.b64encode(jpeg_bytes).decode()
            image_urls.append(f"data:image/jpeg;base64,{b64}")

        doc.close()
        logger.info(
            f"Converted {len(image_urls)} PDF pages to JPEG images for vision "
            f"(avg {sum(len(u) for u in image_urls) // max(len(image_urls), 1) // 1024}KB each)"
        )
        return image_urls
    except Exception as e:
        logger.error(f"Failed to convert PDF pages to images: {e}")
        return []


def _extract_excel(data_url: str, filename: str) -> str:
    """Extract content from a base64-encoded Excel file."""
    try:
        import openpyxl

        _, b64_data = data_url.split(",", 1)
        excel_bytes = base64.b64decode(b64_data)

        wb = openpyxl.load_workbook(io.BytesIO(excel_bytes), read_only=True, data_only=True)
        text_parts: list[str] = []

        for ws in wb.worksheets:
            rows: list[str] = []
            rows.append(f"### Sheet: {ws.title}")

            for row in ws.iter_rows(values_only=True):
                values = [str(cell) if cell is not None else "" for cell in row]
                if any(v.strip() for v in values):
                    rows.append("\t".join(values))

            if len(rows) > 1:
                text_parts.append("\n".join(rows))

        wb.close()

        full_text = "\n\n".join(text_parts)
        if len(full_text) > 15000:
            full_text = full_text[:15000] + "\n\n[... truncated ...]"

        logger.info(f"Extracted {len(full_text)} chars from Excel: {filename}")
        return full_text
    except Exception as e:
        logger.error(f"Failed to extract Excel {filename}: {e}")
        return ""
