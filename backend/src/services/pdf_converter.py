"""PDF to Markdown converter.

Extracts text and images from PDF files and converts them to markdown format
suitable for the BOM agent to read.
"""

import hashlib
from pathlib import Path

try:
    import fitz  # PyMuPDF legacy import
except ImportError:
    import pymupdf as fitz  # PyMuPDF >= 1.24
from loguru import logger


def pdf_to_markdown(pdf_path: Path, output_dir: Path) -> Path:
    """Convert a PDF file to markdown with extracted images.

    Args:
        pdf_path: Path to the source PDF file
        output_dir: Directory to write the .md file and images

    Returns:
        Path to the generated .md file
    """
    doc = fitz.open(str(pdf_path))
    stem = pdf_path.stem
    artifacts_dir = output_dir / f"{stem}_artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    md_lines: list[str] = []
    image_index = 0

    for page_num, page in enumerate(doc):
        # Extract text
        text = page.get_text("text")
        if text.strip():
            md_lines.append(text.strip())
            md_lines.append("")

        # Extract images
        for img_info in page.get_images(full=True):
            try:
                xref = img_info[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # Generate unique filename
                img_hash = hashlib.sha256(image_bytes).hexdigest()[:16]
                img_filename = f"image_{image_index:06d}_{img_hash}.{image_ext}"
                img_path = artifacts_dir / img_filename

                with open(img_path, "wb") as f:
                    f.write(image_bytes)

                # Add image reference in markdown
                relative_img_path = f"{stem}_artifacts/{img_filename}"
                md_lines.append(f"![Image]({relative_img_path})")
                md_lines.append("")
                image_index += 1
            except Exception as e:
                logger.warning(f"Failed to extract image from page {page_num}: {e}")

    doc.close()

    # Write markdown file
    md_path = output_dir / f"{stem}.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    logger.info(f"Converted {pdf_path.name} -> {md_path.name} ({image_index} images)")
    return md_path


def extract_product_code_from_filename(filename: str) -> str:
    """Extract a product code from a PDF filename.

    Examples:
        "MES24xx_datasheet_10.4.2.1_en.pdf" -> "MES24xx"
        "SFP-10G-LR_datasheet.pdf" -> "SFP-10G-LR"
        "Bypass-Product-Line-Datasheet.pdf" -> "Bypass-Product-Line"
    """
    stem = Path(filename).stem

    # Try to extract code before common suffixes
    suffixes_to_strip = ["_datasheet", "_Datasheet", "-Datasheet", "-datasheet",
                         "_spec", "_Spec", "-spec", "-Spec"]
    for suffix in suffixes_to_strip:
        if suffix in stem:
            stem = stem[:stem.index(suffix)]
            break

    # Strip version numbers at the end (e.g. _10.4.2.1_en)
    parts = stem.split("_")
    # Keep parts that don't look like version numbers or language codes
    cleaned = []
    for part in parts:
        if part.replace(".", "").isdigit():
            break
        if len(part) == 2 and part.isalpha():  # language code like "en"
            continue
        cleaned.append(part)

    return "-".join(cleaned) if cleaned else stem


async def extract_product_codes_from_content(md_content: str, filename: str) -> list[str]:
    """Use LLM to extract all product codes/model numbers from datasheet content.

    Args:
        md_content: The markdown text content of the converted PDF
        filename: Original PDF filename for context

    Returns:
        List of product codes found in the document
    """
    from src.services.llms.models import get_model
    from langchain_core.messages import HumanMessage, SystemMessage
    from pydantic import BaseModel

    class ExtractedProducts(BaseModel):
        """List of product codes extracted from a datasheet."""
        codes: list[str]

    # Take first 3000 chars to avoid token limits while getting key info
    preview = md_content[:3000]

    system_prompt = """You are a product code extractor. Given the content of a product datasheet, 
extract ALL specific product model numbers/codes mentioned in the document.

Rules:
- Extract exact model numbers as they appear (e.g. "MES2424 AC", "MES2424P AC", "MES2448 AC")
- Include all variants (AC/DC, different port counts, PoE versions, etc.)
- Do NOT include generic series names that aren't actual orderable products (e.g. "MES24xx" is a series, not a product)
- Do NOT include component part numbers, SFP module codes, or accessories — only the main products
- If the document is about a product family, list each specific model separately
- Keep the exact formatting from the document (spaces, hyphens, etc.)"""

    user_prompt = f"""Extract all product model codes from this datasheet.
Filename: {filename}

Content:
{preview}"""

    try:
        llm = get_model("services/datasheet_matcher/default")
        structured_llm = llm.with_structured_output(ExtractedProducts)
        result = await structured_llm.ainvoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ])
        codes = [c.strip() for c in result.codes if c.strip()]
        logger.info(f"LLM extracted {len(codes)} product codes from {filename}: {codes}")
        return codes
    except Exception as e:
        logger.warning(f"LLM product extraction failed for {filename}: {e}")
        # Fallback to filename-based extraction
        return [extract_product_code_from_filename(filename)]
