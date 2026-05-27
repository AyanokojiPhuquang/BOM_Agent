"""Datasheets upload and management router.

Allows uploading a folder of product datasheets directly from the browser.
Expected folder structure:
    SFP/
        SFP-10G-LR/
            SFP-10G-LR.md
            SFP-10G-LR_artifacts/
                image_001.png
        SFP-25G-SR/
            ...
    QSFP/
        ...

After upload, the system scans the extracted files and creates/updates
product records in the database so the BOM agent can reference them.
"""

import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from loguru import logger
from pydantic import BaseModel

from src.app.auth import get_current_user
from src.configs import SETTINGS
from src.db.database import get_manual_db_session
from src.db.models.nhanh import NhanhProduct
from src.db.models.users import User
from sqlmodel import select

router = APIRouter(prefix="/datasheets", tags=["datasheets"])


# --- Response schemas ---


class DatasheetProductItem(BaseModel):
    code: str
    datasheet_path: str
    category: str


class UploadDatasheetsResponse(BaseModel):
    message: str
    total_files: int
    total_products_created: int
    total_products_updated: int
    products: list[DatasheetProductItem]


class DatasheetListResponse(BaseModel):
    total: int
    categories: dict[str, int]
    products: list[DatasheetProductItem]


class DeleteDatasheetsResponse(BaseModel):
    message: str
    deleted_files: int
    deleted_products: int


# --- Helpers ---


def _scan_datasheets_dir(datasheets_dir: Path) -> list[dict]:
    """Scan the datasheets directory and return product info."""
    if not datasheets_dir.exists():
        return []

    products = []
    for md_file in datasheets_dir.rglob("*.md"):
        relative = md_file.relative_to(datasheets_dir)
        parts = relative.parts
        if len(parts) < 2:
            continue

        category = parts[0]  # e.g. SFP, QSFP, AOC
        folder_name = parts[-2]  # e.g. SFP-10G-LR

        products.append({
            "code": folder_name.strip(),
            "datasheet_path": str(relative),
            "category": category,
        })

    return products


async def _sync_products_from_datasheets(products: list[dict]) -> tuple[int, int]:
    """Create or update NhanhProduct records from scanned datasheets.

    Returns (created_count, updated_count).
    """
    created = 0
    updated = 0

    async with get_manual_db_session() as session:
        # Get all existing products by code
        existing_codes = {}
        result = await session.execute(select(NhanhProduct))
        for p in result.scalars().all():
            existing_codes[p.code.strip().upper()] = p

        # Find the max nhanh_id to generate new ones
        max_nhanh_id = max(
            (p.nhanh_id for p in existing_codes.values()),
            default=40000000,
        )

        for product_info in products:
            code = product_info["code"].strip()
            key = code.upper()
            datasheet_path = product_info["datasheet_path"]

            if key in existing_codes:
                # Update datasheet_path if changed
                existing = existing_codes[key]
                if existing.datasheet_path != datasheet_path:
                    existing.datasheet_path = datasheet_path
                    session.add(existing)
                    updated += 1
            else:
                # Create new product
                max_nhanh_id += 1
                new_product = NhanhProduct(
                    nhanh_id=max_nhanh_id,
                    name=code,
                    code=code,
                    datasheet_path=datasheet_path,
                    status=1,
                    remain=0,
                    available=0,
                    price=0,
                )
                session.add(new_product)
                existing_codes[key] = new_product
                created += 1

        await session.commit()

    return created, updated


# --- Endpoints ---


@router.post("/upload", response_model=UploadDatasheetsResponse)
async def upload_datasheets(
    files: list[UploadFile] = File(...),
    paths: list[str] = Form(default=[]),
    replace: bool = False,
    current_user: User = Depends(get_current_user),
):
    """Upload a folder of product datasheets.

    The frontend sends all files from the selected folder along with their
    relative paths. The backend recreates the folder structure on disk.

    Args:
        files: List of files from the folder
        paths: Corresponding relative paths (e.g. "SFP/SFP-10G-LR/SFP-10G-LR.md")
        replace: If true, clears existing datasheets before saving.
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided.",
        )

    # If paths not provided or mismatch, try to use filenames
    if len(paths) != len(files):
        # Fallback: use the filename as-is (flat upload)
        paths = [f.filename or f"file_{i}" for i, f in enumerate(files)]

    # Security: check for path traversal
    for p in paths:
        if "/../" in p or p.startswith("../") or p.endswith("/.."):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid path: {p}",
            )

    # Strip leading root folder from webkitRelativePath
    # e.g. "datasheets/SFP/SFP-10G-LR/file.md" -> "SFP/SFP-10G-LR/file.md"
    cleaned_paths = []
    for p in paths:
        p = p.lstrip("/")
        parts = Path(p).parts
        # If first part looks like the selected folder name (not a category),
        # strip it. Categories are known short names like SFP, QSFP, AOC, DAC, etc.
        if len(parts) > 2:
            cleaned_paths.append(str(Path(*parts[1:])) if len(parts) > 2 else p)
        else:
            cleaned_paths.append(p)

    datasheets_dir = Path(SETTINGS.datasheets_dir).resolve()

    # Optionally clear existing datasheets
    if replace and datasheets_dir.exists():
        shutil.rmtree(datasheets_dir)
        logger.info("Cleared existing datasheets directory")

    datasheets_dir.mkdir(parents=True, exist_ok=True)

    # Save files preserving folder structure
    saved_count = 0
    for file, rel_path in zip(files, cleaned_paths):
        # Skip hidden/system files
        if any(part.startswith(".") or part == "__MACOSX" for part in Path(rel_path).parts):
            continue

        target_path = datasheets_dir / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)

        content = await file.read()
        with open(target_path, "wb") as f:
            f.write(content)
        saved_count += 1

    logger.info(f"Saved {saved_count} files to {datasheets_dir}")

    # Scan and sync products
    scanned = _scan_datasheets_dir(datasheets_dir)
    created, updated = await _sync_products_from_datasheets(scanned)

    logger.info(f"Synced products: {created} created, {updated} updated")

    return UploadDatasheetsResponse(
        message=f"Successfully uploaded {saved_count} files. {created} products created, {updated} updated.",
        total_files=saved_count,
        total_products_created=created,
        total_products_updated=updated,
        products=[
            DatasheetProductItem(
                code=p["code"],
                datasheet_path=p["datasheet_path"],
                category=p["category"],
            )
            for p in scanned
        ],
    )


@router.get("/", response_model=DatasheetListResponse)
async def list_datasheets(
    current_user: User = Depends(get_current_user),
):
    """List all available datasheets and their product mappings."""
    datasheets_dir = Path(SETTINGS.datasheets_dir).resolve()
    scanned = _scan_datasheets_dir(datasheets_dir)

    categories: dict[str, int] = {}
    for p in scanned:
        categories[p["category"]] = categories.get(p["category"], 0) + 1

    return DatasheetListResponse(
        total=len(scanned),
        categories=categories,
        products=[
            DatasheetProductItem(
                code=p["code"],
                datasheet_path=p["datasheet_path"],
                category=p["category"],
            )
            for p in scanned
        ],
    )


@router.delete("/", response_model=DeleteDatasheetsResponse)
async def delete_all_datasheets(
    current_user: User = Depends(get_current_user),
):
    """Delete all datasheets and their associated product records."""
    datasheets_dir = Path(SETTINGS.datasheets_dir).resolve()

    # Count files before deletion
    deleted_files = 0
    if datasheets_dir.exists():
        for f in datasheets_dir.rglob("*"):
            if f.is_file():
                deleted_files += 1
        shutil.rmtree(datasheets_dir)
    datasheets_dir.mkdir(parents=True, exist_ok=True)

    # Remove product records that have datasheet_path
    deleted_products = 0
    async with get_manual_db_session() as session:
        result = await session.execute(
            select(NhanhProduct).where(NhanhProduct.datasheet_path.isnot(None))
        )
        products = result.scalars().all()
        for p in products:
            await session.delete(p)
            deleted_products += 1
        await session.commit()

    logger.info(f"Deleted {deleted_files} files and {deleted_products} product records")

    return DeleteDatasheetsResponse(
        message="All datasheets and associated products have been deleted.",
        deleted_files=deleted_files,
        deleted_products=deleted_products,
    )


# --- Individual product management ---


class ProductDetailResponse(BaseModel):
    code: str
    datasheet_path: str
    category: str
    content_preview: str
    file_size: int
    has_images: bool
    image_count: int


@router.get("/products/{product_code}", response_model=ProductDetailResponse)
async def get_product_detail(
    product_code: str,
    current_user: User = Depends(get_current_user),
):
    """Get details of a specific product datasheet."""
    datasheets_dir = Path(SETTINGS.datasheets_dir).resolve()
    scanned = _scan_datasheets_dir(datasheets_dir)

    product = next((p for p in scanned if p["code"] == product_code), None)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{product_code}' not found.",
        )

    md_path = datasheets_dir / product["datasheet_path"]
    content = ""
    file_size = 0
    if md_path.exists():
        content = md_path.read_text(encoding="utf-8")
        file_size = md_path.stat().st_size

    # Check for images
    artifacts_dir = md_path.parent / f"{md_path.stem}_artifacts"
    image_count = 0
    if artifacts_dir.exists():
        image_count = len(list(artifacts_dir.glob("*.png"))) + len(list(artifacts_dir.glob("*.jpg")))

    return ProductDetailResponse(
        code=product["code"],
        datasheet_path=product["datasheet_path"],
        category=product["category"],
        content_preview=content[:500],
        file_size=file_size,
        has_images=image_count > 0,
        image_count=image_count,
    )


@router.delete("/products/{product_code}")
async def delete_product(
    product_code: str,
    current_user: User = Depends(get_current_user),
):
    """Delete a specific product's datasheet and DB record."""
    datasheets_dir = Path(SETTINGS.datasheets_dir).resolve()
    scanned = _scan_datasheets_dir(datasheets_dir)

    product = next((p for p in scanned if p["code"] == product_code), None)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{product_code}' not found.",
        )

    # Delete the product folder from disk
    md_path = datasheets_dir / product["datasheet_path"]
    product_folder = md_path.parent
    if product_folder.exists():
        shutil.rmtree(product_folder)

    # Remove empty parent category folder
    category_folder = product_folder.parent
    if category_folder.exists() and not any(category_folder.iterdir()):
        category_folder.rmdir()

    # Delete DB record
    async with get_manual_db_session() as session:
        result = await session.execute(
            select(NhanhProduct).where(NhanhProduct.code == product_code)
        )
        db_product = result.scalars().first()
        if db_product:
            await session.delete(db_product)
            await session.commit()

    return {"message": f"Product '{product_code}' deleted successfully."}


# --- PDF Upload ---


class PdfUploadResponse(BaseModel):
    message: str
    total_pdfs_processed: int
    total_products_created: int
    total_products_updated: int
    products: list[DatasheetProductItem]
    errors: list[str]


@router.post("/upload-pdf", response_model=PdfUploadResponse)
async def upload_pdf_datasheets(
    files: list[UploadFile] = File(...),
    category: str = Form(default="PDF"),
    current_user: User = Depends(get_current_user),
):
    """Upload PDF files containing product datasheets.

    Each PDF is converted to markdown and stored in the datasheets directory.
    LLM extracts all product codes from the content, creating a DB record
    for each so the BOM agent can find them.

    Args:
        files: One or more PDF files
        category: Category folder name (default: "PDF"). Used to organize files.
    """
    from src.services.pdf_converter import (
        pdf_to_markdown,
        extract_product_code_from_filename,
        extract_product_codes_from_content,
    )

    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided.",
        )

    datasheets_dir = Path(SETTINGS.datasheets_dir).resolve()
    datasheets_dir.mkdir(parents=True, exist_ok=True)

    processed = 0
    errors: list[str] = []
    all_new_products: list[dict] = []

    for file in files:
        filename = file.filename or "unknown.pdf"

        # Skip non-PDF files
        if not filename.lower().endswith(".pdf"):
            errors.append(f"Skipped non-PDF file: {filename}")
            continue

        try:
            # Use filename-based code as folder name
            folder_code = extract_product_code_from_filename(filename)
            product_dir = datasheets_dir / category / folder_code
            product_dir.mkdir(parents=True, exist_ok=True)

            # Save PDF temporarily and convert
            temp_pdf = product_dir / filename
            content = await file.read()
            with open(temp_pdf, "wb") as f:
                f.write(content)

            # Convert PDF to markdown
            md_path = pdf_to_markdown(temp_pdf, product_dir)

            # Keep the original PDF for download

            # Extract product codes using LLM
            md_content = md_path.read_text(encoding="utf-8")
            codes = await extract_product_codes_from_content(md_content, filename)

            # If LLM returns nothing, fallback to filename
            if not codes:
                codes = [folder_code]

            # Create product records for each extracted code
            relative_path = str(md_path.relative_to(datasheets_dir))
            for code in codes:
                all_new_products.append({
                    "code": code,
                    "datasheet_path": relative_path,
                    "category": category,
                })

            processed += 1
            logger.info(f"Processed PDF: {filename} -> {len(codes)} products: {codes}")

        except Exception as e:
            errors.append(f"Failed to process {filename}: {str(e)}")
            logger.error(f"PDF processing error for {filename}: {e}")

    # Sync extracted products to DB
    created, updated = await _sync_products_from_datasheets(all_new_products)

    return PdfUploadResponse(
        message=f"Processed {processed} PDF(s). Found {len(all_new_products)} products. {created} created, {updated} updated.",
        total_pdfs_processed=processed,
        total_products_created=created,
        total_products_updated=updated,
        products=[
            DatasheetProductItem(
                code=p["code"],
                datasheet_path=p["datasheet_path"],
                category=p["category"],
            )
            for p in all_new_products
        ],
        errors=errors,
    )


# --- PDF Download ---


class PdfFileItem(BaseModel):
    filename: str
    category: str
    size: int
    download_url: str


class PdfListResponse(BaseModel):
    total: int
    files: list[PdfFileItem]


@router.get("/pdfs", response_model=PdfListResponse)
async def list_uploaded_pdfs(
    current_user: User = Depends(get_current_user),
):
    """List all uploaded PDF files available for download."""
    datasheets_dir = Path(SETTINGS.datasheets_dir).resolve()
    files = []

    if datasheets_dir.exists():
        for pdf_file in datasheets_dir.rglob("*.pdf"):
            relative = pdf_file.relative_to(datasheets_dir)
            parts = relative.parts
            category = parts[0] if len(parts) > 1 else "general"
            files.append(PdfFileItem(
                filename=pdf_file.name,
                category=category,
                size=pdf_file.stat().st_size,
                download_url=f"/api/datasheets/pdfs/{relative}",
            ))

    return PdfListResponse(total=len(files), files=files)


@router.get("/pdfs/{file_path:path}")
async def download_pdf(
    file_path: str,
    current_user: User = Depends(get_current_user),
):
    """Download an uploaded PDF file."""
    from fastapi.responses import FileResponse

    if ".." in file_path:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid path")

    datasheets_dir = Path(SETTINGS.datasheets_dir).resolve()
    full_path = datasheets_dir / file_path

    if not full_path.exists() or not full_path.suffix == ".pdf":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF not found")

    return FileResponse(
        path=str(full_path),
        media_type="application/pdf",
        filename=full_path.name,
    )


@router.delete("/pdfs/{file_path:path}")
async def delete_pdf(
    file_path: str,
    current_user: User = Depends(get_current_user),
):
    """Delete an uploaded PDF file."""
    if ".." in file_path:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid path")

    datasheets_dir = Path(SETTINGS.datasheets_dir).resolve()
    full_path = datasheets_dir / file_path

    if not full_path.exists() or not full_path.suffix == ".pdf":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF not found")

    full_path.unlink()
    return {"message": f"PDF '{full_path.name}' deleted successfully."}
