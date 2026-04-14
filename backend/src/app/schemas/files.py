from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Folder schemas
# ---------------------------------------------------------------------------


class CreateFolderRequest(BaseModel):
    name: str
    parent_id: str | None = None


class UpdateFolderRequest(BaseModel):
    name: str


class FolderResponse(BaseModel):
    id: str
    name: str
    parent_id: str | None
    created_by: str
    created_at: int
    updated_at: int


# ---------------------------------------------------------------------------
# File schemas
# ---------------------------------------------------------------------------


class UpdateFileRequest(BaseModel):
    name: str | None = None
    folder_id: str | None = None
    tags: list[str] | None = None
    metadata: dict[str, str] | None = None


class FileResponse(BaseModel):
    id: str
    name: str
    original_name: str
    mime_type: str
    size: int
    folder_id: str | None
    status: str
    uploaded_by: str
    tags: list[str]
    metadata: dict[str, str]
    created_at: int
    updated_at: int


class FileListResponse(BaseModel):
    items: list[FileResponse]
    folders: list[FolderResponse]
    total: int
    breadcrumb: list[FolderResponse]
