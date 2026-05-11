"""BOM history management router.

Lists generated BOM files and allows downloading/deleting them.
"""

import os
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.app.auth import get_current_user
from src.db.models.users import User

router = APIRouter(prefix="/boms", tags=["boms"])

BOM_DIR = Path("data/generated_boms")


class BomFileItem(BaseModel):
    filename: str
    size: int
    created_at: int  # epoch ms
    download_url: str


class BomListResponse(BaseModel):
    total: int
    items: list[BomFileItem]


@router.get("/", response_model=BomListResponse)
async def list_boms(
    current_user: User = Depends(get_current_user),
):
    """List all generated BOM files, newest first."""
    bom_dir = BOM_DIR.resolve()
    if not bom_dir.exists():
        return BomListResponse(total=0, items=[])

    items = []
    for f in sorted(bom_dir.iterdir(), reverse=True):
        if f.is_file() and f.suffix == ".xlsx":
            stat = f.stat()
            items.append(BomFileItem(
                filename=f.name,
                size=stat.st_size,
                created_at=int(stat.st_mtime * 1000),
                download_url=f"/api/files/boms/{f.name}",
            ))

    return BomListResponse(total=len(items), items=items)


@router.delete("/{filename}")
async def delete_bom(
    filename: str,
    current_user: User = Depends(get_current_user),
):
    """Delete a specific BOM file."""
    # Security: prevent path traversal
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid filename")

    filepath = BOM_DIR.resolve() / filename
    if not filepath.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BOM file not found")

    os.remove(filepath)
    return {"message": f"BOM '{filename}' deleted successfully."}
