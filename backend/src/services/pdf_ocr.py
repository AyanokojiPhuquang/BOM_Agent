"""Vision-based OCR for scanned PDFs using a strong, large-context model.

Some uploaded tender documents are scanned PDFs that carry a broken embedded
text layer. Plain text extraction (pdfplumber) returns fragmented junk that
misleads the agent (missing rows, wrong quantities). For those files we render
each page to an image and ask a dedicated vision model to transcribe the pages
into clean, structured Markdown — preserving tables so every line item survives.

The model is configured under the ``services/pdf_ocr/default`` group
(OpenRouter, e.g. google/gemini-2.5-pro) and is separate from the main
conversational agent so we can use a stronger/larger-context model just here.
"""

from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger

from src.services.llms.models import get_model

_OCR_MODEL = "services/pdf_ocr/default"

# Guard: if the transcription is shorter than this, treat OCR as failed and let
# the caller fall back to sending raw page images to the agent.
_MIN_USABLE_OCR_CHARS = 40

_OCR_SYSTEM_PROMPT = (
    "You are a precise document transcription engine. You are given images of "
    "the pages of a scanned document (often a Vietnamese procurement/tender "
    "'gói thầu' with hardware specification tables).\n\n"
    "Transcribe EVERYTHING you see into clean Markdown, faithfully and "
    "completely. Rules:\n"
    "- Reconstruct every table as a Markdown table. Keep columns aligned to the "
    "correct rows; do NOT merge or drop rows.\n"
    "- Capture EVERY line item / product row. If the table lists 10 items, your "
    "output MUST contain all 10 rows.\n"
    "- Preserve numbers exactly: quantities, distances (e.g. 10km, 40km, 120km), "
    "data rates (1G/10G/40G/100G), part numbers, wavelengths.\n"
    "- Preserve the original language (Vietnamese) text; do not translate.\n"
    "- Do not summarize, interpret, or invent product codes. Only transcribe.\n"
    "- If a cell is unreadable, write [?] rather than guessing.\n"
    "Output only the transcribed Markdown, no commentary."
)

_OCR_USER_TEXT = (
    "Transcribe all pages of this document into complete, structured Markdown. "
    "Make sure every row of every specification table is included."
)


async def ocr_pdf_images(image_urls: list[str], filename: str = "") -> str:
    """Transcribe scanned PDF page images into clean Markdown.

    Args:
        image_urls: base64 ``data:image/...`` URLs, one per page.
        filename: original filename, for logging/context only.

    Returns:
        Transcribed Markdown text, or an empty string if OCR failed or produced
        nothing usable (caller should then fall back to raw-image vision).
    """
    if not image_urls:
        return ""

    content: list[dict] = [{"type": "text", "text": _OCR_USER_TEXT}]
    for url in image_urls:
        content.append({"type": "image_url", "image_url": {"url": url}})

    messages = [
        SystemMessage(content=_OCR_SYSTEM_PROMPT),
        HumanMessage(content=content),
    ]

    try:
        model = get_model(_OCR_MODEL)
        response = await model.ainvoke(messages)
    except Exception as e:
        logger.error(f"PDF OCR model call failed for {filename!r}: {e}")
        return ""

    text = _message_text(response)
    if len(text.strip()) < _MIN_USABLE_OCR_CHARS:
        logger.warning(
            f"PDF OCR for {filename!r} produced too little text "
            f"({len(text.strip())} chars); treating as failed."
        )
        return ""

    logger.info(
        f"PDF OCR for {filename!r}: transcribed {len(image_urls)} page(s) "
        f"into {len(text)} chars of Markdown."
    )
    return text.strip()


def _message_text(response) -> str:
    """Extract plain text from a LangChain chat model response."""
    content = getattr(response, "content", response)
    if isinstance(content, str):
        return content
    # Some providers return a list of content blocks.
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "".join(parts)
    return str(content)
