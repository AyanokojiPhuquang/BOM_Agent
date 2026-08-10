"""Tool to add a product datasheet by giving a product page URL.

Fetches the page, uses an LLM to locate the datasheet download link
(layout-agnostic — works across differently-structured sites), downloads it,
and runs it through the same processing pipeline as a direct PDF upload so the
extracted products become available to the BOM assistant.
"""

import shutil
from pathlib import Path

from langchain_core.tools import tool
from loguru import logger
from pydantic import BaseModel, Field

from src.configs import SETTINGS


class AddDatasheetFromUrlInput(BaseModel):
    """Input schema for the add_datasheet_from_url tool."""

    url: str = Field(
        description="The product page URL that contains a datasheet download link/button."
    )


@tool(args_schema=AddDatasheetFromUrlInput)
async def add_datasheet_from_url(url: str) -> str:
    """Add a product datasheet into the system from a product page URL.

    Use this when a user provides a link to a product page and wants its
    datasheet imported. The system locates the datasheet download link on the
    page using AI, downloads it, extracts the product specifications, and stores
    them so the products can be used in BOM generation and datasheet lookups.

    Args:
        url: The product page URL containing the datasheet download link.

    Returns:
        A summary of the imported products, or an error message.
    """
    from src.app.routers.datasheets import process_datasheet_file
    from src.services.datasheet_scraper import (
        DatasheetScrapeError,
        download_datasheet,
        find_datasheet_url,
    )
    from src.services.pdf_converter import extract_product_code_from_filename

    url = (url or "").strip()
    if not url:
        return "No URL provided."

    category = "WebScraped"

    try:
        selection = await find_datasheet_url(url)
        if not selection.found or not selection.url:
            return (
                "Không tìm thấy link tải datasheet trên trang này. "
                f"{selection.reason}".strip()
            )

        datasheets_dir = Path(SETTINGS.datasheets_dir).resolve()
        tmp_dir = datasheets_dir / category / "_incoming"
        downloaded = await download_datasheet(selection.url, tmp_dir)

        if not downloaded.filename.lower().endswith(".pdf"):
            downloaded.path.unlink(missing_ok=True)
            return (
                f"Đã tìm thấy tài liệu ('{downloaded.filename}') nhưng không phải PDF. "
                "Hiện chỉ hỗ trợ datasheet dạng PDF."
            )

        folder_code = extract_product_code_from_filename(downloaded.filename)
        product_dir = datasheets_dir / category / folder_code
        product_dir.mkdir(parents=True, exist_ok=True)
        final_path = product_dir / downloaded.filename
        shutil.move(str(downloaded.path), str(final_path))
        if tmp_dir.exists() and not any(tmp_dir.iterdir()):
            tmp_dir.rmdir()

        created, updated, records = await process_datasheet_file(
            final_path, category, datasheets_dir
        )
    except DatasheetScrapeError as e:
        logger.error(f"Datasheet scrape failed for {url}: {e}")
        return f"Không thể xử lý datasheet từ URL: {e}"
    except Exception as e:
        logger.error(f"Unexpected error adding datasheet from {url}: {e}")
        return f"Đã xảy ra lỗi khi xử lý datasheet từ URL: {e}"

    if not records:
        return (
            f"Đã tải datasheet '{downloaded.filename}' nhưng không trích xuất được "
            "sản phẩm nào."
        )

    codes = ", ".join(r["code"] for r in records)
    return (
        f"Đã import datasheet '{downloaded.filename}' từ {selection.url}. "
        f"{created} sản phẩm được tạo mới, {updated} được cập nhật. "
        f"Sản phẩm: {codes}"
    )
