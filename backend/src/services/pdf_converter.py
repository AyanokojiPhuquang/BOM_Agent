"""PDF to Markdown converter with structured product extraction.

Extracts text and images from PDF files, converts them to markdown,
then uses LLM to extract structured product specs for each product
found in the document.
"""

import hashlib
from pathlib import Path

try:
    import fitz  # PyMuPDF legacy import
except ImportError:
    import pymupdf as fitz  # PyMuPDF >= 1.24
from loguru import logger
from pydantic import BaseModel, Field


# --- Pydantic schemas for LLM extraction ---


class ExtractedProductSpec(BaseModel):
    """Structured specs for a single product extracted from a datasheet."""

    code: str = Field(description="Product code / SKU / model number, e.g. MES3500I-10P, SFP-10G-LR")
    name: str = Field(default="", description="Full product name if available")
    brand: str = Field(default="", description="Manufacturer/brand, e.g. Eltex, ModuleTek, Starview")
    description: str = Field(default="", description="Short product description in Vietnamese")
    data_rate: str = Field(default="", description="Data rate: 1G, 10G, 25G, 40G, 100G, or N/A if not applicable")
    fiber_type: str = Field(default="", description="Fiber type: single-mode, multi-mode, copper, or N/A")
    wavelength: str = Field(default="", description="Wavelength: e.g. 1310nm, 850nm, or N/A if not applicable")
    max_distance: str = Field(default="", description="Max distance: e.g. 10km, 300m, or N/A if not applicable")
    connector: str = Field(default="", description="Connector type: LC Duplex, MPO/MTP, RJ-45, SC, or N/A")
    main_device: str = Field(default="N/A", description="Compatible main device — always default to N/A, user will edit manually")
    category: str = Field(default="", description="Product category: SFP, QSFP, AOC, DAC, Switch, Media Converter, etc.")
    raw_specs: str = Field(default="", description="Any additional important specs not covered above (free text)")


class ExtractedProducts(BaseModel):
    """All products extracted from a single datasheet document."""

    products: list[ExtractedProductSpec]


# --- PDF conversion ---


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

    # Use pdfplumber for text extraction (handles more font types than PyMuPDF)
    import pdfplumber
    try:
        with pdfplumber.open(str(pdf_path)) as plumber_pdf:
            for page_num, plumber_page in enumerate(plumber_pdf.pages):
                text = plumber_page.extract_text() or ""
                if text.strip():
                    md_lines.append(text.strip())
                    md_lines.append("")
    except Exception as e:
        logger.warning(f"pdfplumber failed, falling back to PyMuPDF for text: {e}")
        for page_num, page in enumerate(doc):
            text = page.get_text("text")
            if text.strip():
                md_lines.append(text.strip())
                md_lines.append("")

    # Use PyMuPDF for image extraction (pdfplumber doesn't extract images well)
    for page_num, page in enumerate(doc):
        for img_info in page.get_images(full=True):
            try:
                xref = img_info[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                img_hash = hashlib.sha256(image_bytes).hexdigest()[:16]
                img_filename = f"image_{image_index:06d}_{img_hash}.{image_ext}"
                img_path = artifacts_dir / img_filename

                with open(img_path, "wb") as f:
                    f.write(image_bytes)

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


# --- Product code extraction (simple fallback) ---


def extract_product_code_from_filename(filename: str) -> str:
    """Extract a product code from a PDF filename.

    Examples:
        "MES24xx_datasheet_10.4.2.1_en.pdf" -> "MES24xx"
        "SFP-10G-LR_datasheet.pdf" -> "SFP-10G-LR"
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
    cleaned = []
    for part in parts:
        if part.replace(".", "").isdigit():
            break
        if len(part) == 2 and part.isalpha():  # language code like "en"
            continue
        cleaned.append(part)

    return "-".join(cleaned) if cleaned else stem


# --- LLM-based structured extraction ---


_EXTRACTION_SYSTEM_PROMPT = """You are a product specification extractor for a Vietnamese IT/telecommunications equipment distributor.

Given the content of a product datasheet PDF, extract ALL specific products mentioned with their full technical specifications.

## Rules

1. **Product codes must be REAL orderable model numbers.** Look for an "Ordering Information" table, "Order Information" table, "Model" column, or "Part Number" / "P/N" section — these contain the actual product codes customers use to order. Examples of real product codes: `6002FE`, `6101GE-SFP`, `SFP-10G-LR`, `UBMSBD-25`, `UBMSBQD-20`, `CVR-QSFP-SFP10G`.

2. **Do NOT fabricate or generate product codes.** Only extract codes that **explicitly appear as-is** in an ordering table or part number list. Do NOT:
   - Use configuration descriptions (e.g. "1POE+1UTP", "4POE+1SFP") as product codes
   - Generate codes from naming scheme diagrams (e.g. "950XX-XX-XX" patterns)
   - Invent codes by combining a naming prefix with spec values
   If the document shows a naming convention diagram but also has a concrete ordering table — use ONLY the codes from the ordering table.

3. **If no ordering table exists**, look for model numbers in the document header, title, or spec tables. A product code is typically a short alphanumeric string (e.g. `6108GE-SFP`, `P1GMCBPE`, `MES2424B`) — not a long descriptive phrase.

4. **Extract every distinct orderable model.** One PDF may describe multiple products. Create a separate entry for each orderable product code found in the ordering/model table.

5. **Be precise with specs.** Only fill in a field if the information is clearly stated in the document. Use "N/A" for fields that genuinely don't apply to this product type (e.g. wavelength for a copper switch). Leave empty ("") if the info should exist but you can't find it.

6. **Product types and their expected fields:**
   - **Optical transceivers** (SFP, QSFP, XFP): should have data_rate, fiber_type, wavelength, max_distance, connector
   - **Switches/Routers**: data_rate (port speed), connector (port types), fiber_type and wavelength usually "N/A"
   - **Media converters**: data_rate, fiber_type, connector, may have wavelength and distance
   - **Cables** (AOC, DAC): data_rate, max_distance (cable length), connector

7. **Brand/manufacturer:** Extract the actual brand from the document (e.g. Eltex, Cisco, ModuleTek). Do NOT guess.

8. **Description:** Write a concise Vietnamese description of the product. Example: "Switch PoE 8 cổng 10/100/1000M, 1 cổng SFP uplink, IEEE 802.3af/at"

9. **Category:** Classify each product into one of: SFP, QSFP, XFP, AOC, DAC, MPO-MTP, Switch, Router, Media Converter, Other

10. **raw_specs:** Include any important specifications not covered by the structured fields, such as: operating temperature range, power consumption, PoE budget, switching capacity, rack size, etc.

11. **main_device:** Always set to "N/A". This field will be filled in manually by the user later."""


async def extract_product_specs_from_content(
    md_content: str, filename: str
) -> list[ExtractedProductSpec]:
    """Use LLM to extract structured product specifications from datasheet content.

    Args:
        md_content: The markdown text content of the converted PDF
        filename: Original PDF filename for context

    Returns:
        List of extracted product specs
    """
    from src.services.llms.models import get_model
    from langchain_core.messages import HumanMessage, SystemMessage

    # Build the content to send to LLM
    # Strategy: Find "Order Information" / "Ordering" section and prioritize it
    # Also include beginning for brand/context
    ordering_section = ""
    ordering_keywords = ["order information", "ordering information", "part number", "model"]
    
    lines = md_content.split("\n")
    for i, line in enumerate(lines):
        if any(kw in line.lower() for kw in ordering_keywords):
            # Found ordering section — grab from here to end (up to 5000 chars)
            ordering_section = "\n".join(lines[i:])[:5000]
            break

    if ordering_section:
        # Send: beginning (brand/context) + ordering section (actual product codes)
        beginning = md_content[:3000]
        preview = f"{beginning}\n\n[...content omitted...]\n\n## ORDERING / PART NUMBER SECTION (USE THIS FOR PRODUCT CODES):\n{ordering_section}"
    elif len(md_content) <= 10000:
        preview = md_content
    else:
        # Fallback: first 4000 + last 6000
        preview = md_content[:4000] + "\n\n[...middle content omitted...]\n\n" + md_content[-6000:]

    user_prompt = f"""Extract all products and their specifications from this datasheet.
IMPORTANT: If there is an "Order Information" or "Ordering Information" table, extract product codes ONLY from that table. Do NOT generate codes from naming scheme diagrams.

Filename: {filename}

Content:
{preview}"""

    try:
        llm = get_model("services/datasheet_matcher/default")
        structured_llm = llm.with_structured_output(ExtractedProducts)
        result = await structured_llm.ainvoke([
            SystemMessage(content=_EXTRACTION_SYSTEM_PROMPT),
            HumanMessage(content=user_prompt),
        ])
        specs = [s for s in result.products if s.code.strip()]
        logger.info(f"LLM extracted {len(specs)} products from {filename}: {[s.code for s in specs]}")
        return specs
    except Exception as e:
        logger.warning(f"LLM product extraction failed for {filename}: {e}")
        # Fallback: return a single product with code from filename
        code = extract_product_code_from_filename(filename)
        return [ExtractedProductSpec(code=code)]


# Legacy function kept for backward compatibility
async def extract_product_codes_from_content(md_content: str, filename: str) -> list[str]:
    """Extract product codes from content. Returns just the codes."""
    specs = await extract_product_specs_from_content(md_content, filename)
    return [s.code for s in specs]
