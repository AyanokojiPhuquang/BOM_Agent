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
# Text-quality thresholds for detecting a broken/garbled text layer.
# Scanned PDFs with a poor embedded OCR layer often extract as many short,
# fragmented lines (single characters spread across rows). Such text passes a
# naive length check but is useless to the agent, so we route those to vision.
# A "short line" is one with at most this many non-space characters.
GARBLED_SHORT_LINE_MAX_CHARS = 2
# If at least this fraction of non-empty lines are short, treat as garbled.
GARBLED_SHORT_LINE_FRACTION = 0.4
# Only apply the garbled check once there are enough lines to be meaningful.
GARBLED_MIN_LINES = 15


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
    Only returns images for PDFs that don't have usable extractable text.
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


async def extract_scanned_pdf_markdown(images: list) -> tuple[str, list[str]]:
    """OCR scanned/garbled PDFs into clean Markdown via a dedicated vision model.

    For each PDF attachment whose text layer is missing or garbled, render its
    pages to images and transcribe them with the strong OCR model. This yields
    structured Markdown (tables preserved) that is far more reliable for the
    agent than a broken pdfplumber text layer.

    Args:
        images: list of ImageAttachment-like objects.

    Returns:
        A tuple ``(markdown, leftover_image_urls)``:
          * ``markdown``: combined OCR Markdown for all scanned PDFs (may be "").
          * ``leftover_image_urls``: page images for any scanned PDF where OCR
            failed, so the caller can still fall back to raw-image vision.
    """
    # Imported lazily to avoid a heavy import at module load and to keep the
    # text-only extraction path free of LLM dependencies.
    from src.services.pdf_ocr import ocr_pdf_images

    markdown_parts: list[str] = []
    leftover_images: list[str] = []

    for attachment in images:
        name = attachment.name if hasattr(attachment, "name") else attachment.get("name", "")
        data_url = attachment.dataUrl if hasattr(attachment, "dataUrl") else attachment.get("dataUrl", "")

        if not data_url or "," not in data_url:
            continue
        if not name.lower().endswith(".pdf"):
            continue

        _, b64_data = data_url.split(",", 1)
        pdf_bytes = base64.b64decode(b64_data)

        if not _is_scanned_pdf(pdf_bytes):
            continue

        page_images = _pdf_pages_to_images(pdf_bytes)
        if not page_images:
            continue

        ocr_text = await ocr_pdf_images(page_images, filename=name)
        if ocr_text:
            markdown_parts.append(f"## File: {name}\n{ocr_text}")
        else:
            # OCR unavailable/failed — keep raw images for agent vision fallback.
            leftover_images.extend(page_images)

    return "\n\n".join(markdown_parts), leftover_images


def _looks_like_garbled_text(text: str) -> bool:
    """Heuristic: does extracted text look like a broken OCR/text layer?

    Scanned tender documents sometimes carry a low-quality embedded text layer
    that pdfplumber extracts as hundreds of 1-2 character lines (columns torn
    apart). That text is long enough to pass a length check but is unusable.
    We flag it so the caller can fall back to vision instead.

    Returns True only when there are enough lines to judge AND a large share of
    them are extremely short.
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if len(lines) < GARBLED_MIN_LINES:
        return False

    short = sum(1 for ln in lines if len(ln) <= GARBLED_SHORT_LINE_MAX_CHARS)
    fraction = short / len(lines)
    return fraction >= GARBLED_SHORT_LINE_FRACTION


def _is_usable_pdf_text(text: str) -> bool:
    """True if extracted PDF text is both long enough and not garbled."""
    if not text or len(text) <= MIN_CHARS_PER_PAGE:
        return False
    return not _looks_like_garbled_text(text)


def _extract_pdf_smart(data_url: str, filename: str) -> str:
    """Smart PDF extraction: text first, vision fallback for scans.

    Returns extracted text, or a marker indicating pages were sent as images.
    """
    _, b64_data = data_url.split(",", 1)
    pdf_bytes = base64.b64decode(b64_data)

    # Try text extraction first
    text = _extract_pdf_text(pdf_bytes)

    if _is_usable_pdf_text(text):
        # Good text extraction — use it
        if len(text) > 15000:
            text = text[:15000] + "\n\n[... truncated ...]"
        logger.info(f"PDF text extraction successful for {filename}: {len(text)} chars")
        return text

    # Text extraction failed, too sparse, or garbled (broken OCR layer).
    # Treat as a scanned PDF: pages are sent as images separately via image_urls.
    # Do NOT feed the garbled text into the prompt — it misleads the agent.
    reason = "too sparse" if (not text or len(text) <= MIN_CHARS_PER_PAGE) else "garbled/fragmented"
    logger.info(f"PDF {filename} text is {reason}. Falling back to vision.")
    return "[This PDF appears to be scanned/image-based. The page images have been sent for visual analysis.]"


def _is_scanned_pdf(pdf_bytes: bytes) -> bool:
    """Check if a PDF needs vision (no usable extractable text).

    Returns True when the text layer is missing/sparse OR when it is present
    but garbled (a broken embedded OCR layer), so scanned tender tables with
    junk text still get routed to vision.
    """
    text = _extract_pdf_text(pdf_bytes)
    return not _is_usable_pdf_text(text)


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
