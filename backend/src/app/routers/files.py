import json
import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse as StarletteFileResponse

from src.app.auth import get_current_user
from src.app.dependencies import (
    get_file_metadata_repository,
    get_file_repository,
    get_file_tag_repository,
    get_folder_repository,
)
from src.app.schemas.files import (
    CreateFolderRequest,
    FileListResponse,
    FileResponse,
    FolderResponse,
    UpdateFileRequest,
    UpdateFolderRequest,
)
from src.db.models.files import Folder, ManagedFile
from src.db.models.users import User
from src.db.repositories.file import (
    FileMetadataRepository,
    FileRepository,
    FileTagRepository,
    FolderRepository,
)

router = APIRouter()

MANAGED_FILES_DIR = Path("data/managed_files")


def _to_epoch_ms(dt) -> int:
    return int(dt.timestamp() * 1000)


def _folder_to_response(folder: Folder) -> FolderResponse:
    return FolderResponse(
        id=folder.id,
        name=folder.name,
        parent_id=folder.parent_id,
        created_by=folder.created_by,
        created_at=_to_epoch_ms(folder.created_at),
        updated_at=_to_epoch_ms(folder.updated_at),
    )


async def _file_to_response(
    f: ManagedFile,
    tag_repo: FileTagRepository,
    meta_repo: FileMetadataRepository,
) -> FileResponse:
    tags = await tag_repo.get_tags(f.id)
    metadata = await meta_repo.get_metadata(f.id)
    return FileResponse(
        id=f.id,
        name=f.name,
        original_name=f.original_name,
        mime_type=f.mime_type,
        size=f.size,
        folder_id=f.folder_id,
        status=f.status,
        uploaded_by=f.uploaded_by,
        tags=tags,
        metadata=metadata,
        created_at=_to_epoch_ms(f.created_at),
        updated_at=_to_epoch_ms(f.updated_at),
    )


# ---------------------------------------------------------------------------
# Folder endpoints
# ---------------------------------------------------------------------------


@router.post(
    "/file-manager/folders",
    response_model=FolderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_folder(
    request: CreateFolderRequest,
    current_user: User = Depends(get_current_user),
    folder_repo: FolderRepository = Depends(get_folder_repository),
):
    if request.parent_id:
        parent = await folder_repo.get_by_id(request.parent_id)
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent folder not found",
            )

    folder = await folder_repo.create(
        name=request.name,
        parent_id=request.parent_id,
        created_by=current_user.id,
    )
    return _folder_to_response(folder)


@router.put("/file-manager/folders/{folder_id}", response_model=FolderResponse)
async def update_folder(
    folder_id: str,
    request: UpdateFolderRequest,
    folder_repo: FolderRepository = Depends(get_folder_repository),
):
    folder = await folder_repo.update(folder_id, request.name)
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found",
        )
    return _folder_to_response(folder)


@router.delete(
    "/file-manager/folders/{folder_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_folder(
    folder_id: str,
    folder_repo: FolderRepository = Depends(get_folder_repository),
):
    has_children = await folder_repo.has_children(folder_id)
    if has_children:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Folder is not empty. Delete its contents first.",
        )

    deleted = await folder_repo.delete(folder_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found",
        )


# ---------------------------------------------------------------------------
# File endpoints
# ---------------------------------------------------------------------------


@router.get("/file-manager/files", response_model=FileListResponse)
async def list_files(
    folder_id: str | None = None,
    search: str | None = None,
    limit: int = 100,
    offset: int = 0,
    file_repo: FileRepository = Depends(get_file_repository),
    folder_repo: FolderRepository = Depends(get_folder_repository),
    tag_repo: FileTagRepository = Depends(get_file_tag_repository),
    meta_repo: FileMetadataRepository = Depends(get_file_metadata_repository),
):
    files = await file_repo.list_by_folder(folder_id, search, limit, offset)
    total = await file_repo.count_by_folder(folder_id, search)
    folders = await folder_repo.list_by_parent(folder_id)
    breadcrumb = await folder_repo.get_breadcrumb(folder_id)

    return FileListResponse(
        items=[await _file_to_response(f, tag_repo, meta_repo) for f in files],
        folders=[_folder_to_response(f) for f in folders],
        total=total,
        breadcrumb=[_folder_to_response(b) for b in breadcrumb],
    )


@router.post(
    "/file-manager/files/upload",
    response_model=FileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    file: UploadFile = File(...),
    folder_id: str | None = Form(default=None),
    tags: str = Form(default="[]"),
    metadata: str = Form(default="{}"),
    current_user: User = Depends(get_current_user),
    file_repo: FileRepository = Depends(get_file_repository),
    folder_repo: FolderRepository = Depends(get_folder_repository),
    tag_repo: FileTagRepository = Depends(get_file_tag_repository),
    meta_repo: FileMetadataRepository = Depends(get_file_metadata_repository),
):
    # Validate folder exists if provided
    if folder_id:
        parent = await folder_repo.get_by_id(folder_id)
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Folder not found",
            )

    # Parse tags and metadata from JSON strings
    try:
        tag_list: list[str] = json.loads(tags)
    except (json.JSONDecodeError, TypeError):
        tag_list = []

    try:
        meta_dict: dict[str, str] = json.loads(metadata)
    except (json.JSONDecodeError, TypeError):
        meta_dict = {}

    # Save file to disk
    ext = Path(file.filename or "").suffix
    storage_name = f"{uuid.uuid4()}{ext}"
    storage_path = str(MANAGED_FILES_DIR / storage_name)

    MANAGED_FILES_DIR.mkdir(parents=True, exist_ok=True)
    content = await file.read()
    with open(storage_path, "wb") as f:
        f.write(content)

    # Create DB record
    db_file = await file_repo.create(
        name=Path(file.filename or "upload").stem,
        original_name=file.filename or "upload",
        mime_type=file.content_type or "application/octet-stream",
        size=len(content),
        storage_path=storage_path,
        folder_id=folder_id,
        status="ready",
        uploaded_by=current_user.id,
    )

    # Set tags and metadata
    if tag_list:
        await tag_repo.set_tags(db_file.id, tag_list)
    if meta_dict:
        await meta_repo.set_metadata(db_file.id, meta_dict)

    return await _file_to_response(db_file, tag_repo, meta_repo)


@router.get("/file-manager/files/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: str,
    file_repo: FileRepository = Depends(get_file_repository),
    tag_repo: FileTagRepository = Depends(get_file_tag_repository),
    meta_repo: FileMetadataRepository = Depends(get_file_metadata_repository),
):
    f = await file_repo.get_by_id(file_id)
    if not f:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    return await _file_to_response(f, tag_repo, meta_repo)


@router.put("/file-manager/files/{file_id}", response_model=FileResponse)
async def update_file(
    file_id: str,
    request: UpdateFileRequest,
    file_repo: FileRepository = Depends(get_file_repository),
    folder_repo: FolderRepository = Depends(get_folder_repository),
    tag_repo: FileTagRepository = Depends(get_file_tag_repository),
    meta_repo: FileMetadataRepository = Depends(get_file_metadata_repository),
):
    f = await file_repo.get_by_id(file_id)
    if not f:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    # Update basic fields
    fields: dict = {}
    if request.name is not None:
        fields["name"] = request.name
    if request.folder_id is not None:
        # Validate target folder
        target = await folder_repo.get_by_id(request.folder_id)
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target folder not found",
            )
        fields["folder_id"] = request.folder_id

    if fields:
        f = await file_repo.update(file_id, **fields)

    # Update tags
    if request.tags is not None:
        await tag_repo.set_tags(file_id, request.tags)

    # Update metadata
    if request.metadata is not None:
        await meta_repo.set_metadata(file_id, request.metadata)

    return await _file_to_response(f, tag_repo, meta_repo)


@router.delete(
    "/file-manager/files/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_file(
    file_id: str,
    file_repo: FileRepository = Depends(get_file_repository),
):
    f = await file_repo.get_by_id(file_id)
    if not f:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    # Remove physical file
    if os.path.exists(f.storage_path):
        os.remove(f.storage_path)

    await file_repo.delete(file_id)


@router.get("/file-manager/files/{file_id}/download")
async def download_file(
    file_id: str,
    file_repo: FileRepository = Depends(get_file_repository),
):
    f = await file_repo.get_by_id(file_id)
    if not f:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    if not os.path.exists(f.storage_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk",
        )

    return StarletteFileResponse(
        path=f.storage_path,
        media_type=f.mime_type,
        filename=f.original_name,
    )
