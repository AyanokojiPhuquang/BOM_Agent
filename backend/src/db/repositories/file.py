from datetime import datetime, timezone

from sqlalchemy import func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.files import FileMetadata, FileTag, Folder, ManagedFile


# ---------------------------------------------------------------------------
# Folder standalone functions
# ---------------------------------------------------------------------------


async def create_folder(
    session: AsyncSession, name: str, parent_id: str | None, created_by: str
) -> Folder:
    folder = Folder(name=name, parent_id=parent_id, created_by=created_by)
    session.add(folder)
    await session.flush()
    return folder


async def get_folder_by_id(session: AsyncSession, folder_id: str) -> Folder | None:
    result = await session.execute(select(Folder).where(Folder.id == folder_id))
    return result.scalar_one_or_none()


async def list_folders_by_parent(
    session: AsyncSession, parent_id: str | None
) -> list[Folder]:
    result = await session.execute(
        select(Folder)
        .where(Folder.parent_id == parent_id if parent_id else Folder.parent_id.is_(None))
        .order_by(Folder.name)
    )
    return list(result.scalars().all())


async def update_folder(
    session: AsyncSession, folder_id: str, name: str
) -> Folder | None:
    folder = await get_folder_by_id(session, folder_id)
    if not folder:
        return None
    folder.name = name
    folder.updated_at = datetime.now(timezone.utc)
    session.add(folder)
    await session.flush()
    await session.refresh(folder)
    return folder


async def delete_folder(session: AsyncSession, folder_id: str) -> bool:
    folder = await get_folder_by_id(session, folder_id)
    if not folder:
        return False
    await session.delete(folder)
    await session.flush()
    return True


async def folder_has_children(session: AsyncSession, folder_id: str) -> bool:
    file_count = await session.execute(
        select(func.count()).select_from(ManagedFile).where(ManagedFile.folder_id == folder_id)
    )
    if file_count.scalar_one() > 0:
        return True
    sub_count = await session.execute(
        select(func.count()).select_from(Folder).where(Folder.parent_id == folder_id)
    )
    return sub_count.scalar_one() > 0


async def get_folder_breadcrumb(session: AsyncSession, folder_id: str | None) -> list[Folder]:
    breadcrumb: list[Folder] = []
    current_id = folder_id
    while current_id:
        folder = await get_folder_by_id(session, current_id)
        if not folder:
            break
        breadcrumb.append(folder)
        current_id = folder.parent_id
    breadcrumb.reverse()
    return breadcrumb


# ---------------------------------------------------------------------------
# File standalone functions
# ---------------------------------------------------------------------------


async def create_file(
    session: AsyncSession,
    name: str,
    original_name: str,
    mime_type: str,
    size: int,
    storage_path: str,
    folder_id: str | None,
    status: str,
    uploaded_by: str,
) -> ManagedFile:
    f = ManagedFile(
        name=name,
        original_name=original_name,
        mime_type=mime_type,
        size=size,
        storage_path=storage_path,
        folder_id=folder_id,
        status=status,
        uploaded_by=uploaded_by,
    )
    session.add(f)
    await session.flush()
    return f


async def get_file_by_id(session: AsyncSession, file_id: str) -> ManagedFile | None:
    result = await session.execute(
        select(ManagedFile).where(ManagedFile.id == file_id)
    )
    return result.scalar_one_or_none()


async def list_files_by_folder(
    session: AsyncSession,
    folder_id: str | None,
    search: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[ManagedFile]:
    stmt = select(ManagedFile).where(
        ManagedFile.folder_id == folder_id if folder_id else ManagedFile.folder_id.is_(None)
    )
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(ManagedFile.name.ilike(pattern), ManagedFile.original_name.ilike(pattern))
        )
    stmt = stmt.order_by(ManagedFile.created_at.desc()).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def count_files_by_folder(
    session: AsyncSession,
    folder_id: str | None,
    search: str | None = None,
) -> int:
    stmt = select(func.count()).select_from(ManagedFile).where(
        ManagedFile.folder_id == folder_id if folder_id else ManagedFile.folder_id.is_(None)
    )
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            or_(ManagedFile.name.ilike(pattern), ManagedFile.original_name.ilike(pattern))
        )
    result = await session.execute(stmt)
    return result.scalar_one()


async def update_file(
    session: AsyncSession, file_id: str, **fields: str | int | None
) -> ManagedFile | None:
    f = await get_file_by_id(session, file_id)
    if not f:
        return None
    for key, value in fields.items():
        if value is not None and hasattr(f, key):
            setattr(f, key, value)
    f.updated_at = datetime.now(timezone.utc)
    session.add(f)
    await session.flush()
    await session.refresh(f)
    return f


async def delete_file(session: AsyncSession, file_id: str) -> bool:
    f = await get_file_by_id(session, file_id)
    if not f:
        return False
    await session.delete(f)
    await session.flush()
    return True


# ---------------------------------------------------------------------------
# FileTag standalone functions
# ---------------------------------------------------------------------------


async def set_file_tags(
    session: AsyncSession, file_id: str, tags: list[str]
) -> list[FileTag]:
    # Delete existing tags
    existing = await session.execute(
        select(FileTag).where(FileTag.file_id == file_id)
    )
    for tag_obj in existing.scalars().all():
        await session.delete(tag_obj)
    await session.flush()

    new_tags = []
    for tag in dict.fromkeys(tags):  # deduplicate preserving order
        t = FileTag(file_id=file_id, tag=tag)
        session.add(t)
        new_tags.append(t)
    await session.flush()
    return new_tags


async def get_file_tags(session: AsyncSession, file_id: str) -> list[str]:
    result = await session.execute(
        select(FileTag.tag).where(FileTag.file_id == file_id).order_by(FileTag.tag)
    )
    return list(result.scalars().all())


# ---------------------------------------------------------------------------
# FileMetadata standalone functions
# ---------------------------------------------------------------------------


async def set_file_metadata(
    session: AsyncSession, file_id: str, metadata: dict[str, str]
) -> list[FileMetadata]:
    existing = await session.execute(
        select(FileMetadata).where(FileMetadata.file_id == file_id)
    )
    for meta_obj in existing.scalars().all():
        await session.delete(meta_obj)
    await session.flush()

    new_meta = []
    for key, value in metadata.items():
        m = FileMetadata(file_id=file_id, key=key, value=value)
        session.add(m)
        new_meta.append(m)
    await session.flush()
    return new_meta


async def get_file_metadata(session: AsyncSession, file_id: str) -> dict[str, str]:
    result = await session.execute(
        select(FileMetadata).where(FileMetadata.file_id == file_id).order_by(FileMetadata.key)
    )
    return {m.key: m.value for m in result.scalars().all()}


# ---------------------------------------------------------------------------
# Class wrappers
# ---------------------------------------------------------------------------


class FolderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, parent_id: str | None, created_by: str) -> Folder:
        return await create_folder(self.session, name, parent_id, created_by)

    async def get_by_id(self, folder_id: str) -> Folder | None:
        return await get_folder_by_id(self.session, folder_id)

    async def list_by_parent(self, parent_id: str | None) -> list[Folder]:
        return await list_folders_by_parent(self.session, parent_id)

    async def update(self, folder_id: str, name: str) -> Folder | None:
        return await update_folder(self.session, folder_id, name)

    async def delete(self, folder_id: str) -> bool:
        return await delete_folder(self.session, folder_id)

    async def has_children(self, folder_id: str) -> bool:
        return await folder_has_children(self.session, folder_id)

    async def get_breadcrumb(self, folder_id: str | None) -> list[Folder]:
        return await get_folder_breadcrumb(self.session, folder_id)


class FileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        name: str,
        original_name: str,
        mime_type: str,
        size: int,
        storage_path: str,
        folder_id: str | None,
        status: str,
        uploaded_by: str,
    ) -> ManagedFile:
        return await create_file(
            self.session, name, original_name, mime_type, size,
            storage_path, folder_id, status, uploaded_by,
        )

    async def get_by_id(self, file_id: str) -> ManagedFile | None:
        return await get_file_by_id(self.session, file_id)

    async def list_by_folder(
        self, folder_id: str | None, search: str | None = None,
        limit: int = 100, offset: int = 0,
    ) -> list[ManagedFile]:
        return await list_files_by_folder(self.session, folder_id, search, limit, offset)

    async def count_by_folder(
        self, folder_id: str | None, search: str | None = None,
    ) -> int:
        return await count_files_by_folder(self.session, folder_id, search)

    async def update(self, file_id: str, **fields: str | int | None) -> ManagedFile | None:
        return await update_file(self.session, file_id, **fields)

    async def delete(self, file_id: str) -> bool:
        return await delete_file(self.session, file_id)


class FileTagRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def set_tags(self, file_id: str, tags: list[str]) -> list[FileTag]:
        return await set_file_tags(self.session, file_id, tags)

    async def get_tags(self, file_id: str) -> list[str]:
        return await get_file_tags(self.session, file_id)


class FileMetadataRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def set_metadata(self, file_id: str, metadata: dict[str, str]) -> list[FileMetadata]:
        return await set_file_metadata(self.session, file_id, metadata)

    async def get_metadata(self, file_id: str) -> dict[str, str]:
        return await get_file_metadata(self.session, file_id)
