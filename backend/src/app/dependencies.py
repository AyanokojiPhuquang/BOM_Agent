from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db_session
from src.db.repositories.conversation import ConversationRepository
from src.db.repositories.file import (
    FileMetadataRepository,
    FileRepository,
    FileTagRepository,
    FolderRepository,
)
from src.db.repositories.nhanh import NhanhProductRepository, NhanhTokenRepository
from src.db.repositories.user import UserRepository
from src.services.nhanh.service import NhanhService


async def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(session)


async def get_conversation_repository(
    session: AsyncSession = Depends(get_db_session),
) -> ConversationRepository:
    return ConversationRepository(session)


async def get_nhanh_token_repository(
    session: AsyncSession = Depends(get_db_session),
) -> NhanhTokenRepository:
    return NhanhTokenRepository(session)


async def get_nhanh_product_repository(
    session: AsyncSession = Depends(get_db_session),
) -> NhanhProductRepository:
    return NhanhProductRepository(session)


async def get_nhanh_service(
    repo: NhanhTokenRepository = Depends(get_nhanh_token_repository),
) -> NhanhService:
    return NhanhService(repo)


async def get_file_repository(
    session: AsyncSession = Depends(get_db_session),
) -> FileRepository:
    return FileRepository(session)


async def get_folder_repository(
    session: AsyncSession = Depends(get_db_session),
) -> FolderRepository:
    return FolderRepository(session)


async def get_file_tag_repository(
    session: AsyncSession = Depends(get_db_session),
) -> FileTagRepository:
    return FileTagRepository(session)


async def get_file_metadata_repository(
    session: AsyncSession = Depends(get_db_session),
) -> FileMetadataRepository:
    return FileMetadataRepository(session)
