from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.users import User


# --- Standalone functions ---


async def create_user(
    session: AsyncSession,
    email: str,
    name: str,
    hashed_password: str,
    role: str = "user",
) -> User:
    user = User(email=email, name=name, hashed_password=hashed_password, role=role)
    session.add(user)
    await session.flush()
    return user


async def get_user_by_id(session: AsyncSession, user_id: str) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def list_users(
    session: AsyncSession, limit: int = 100, offset: int = 0
) -> list[User]:
    result = await session.execute(
        select(User).order_by(User.created_at.desc()).limit(limit).offset(offset)
    )
    return list(result.scalars().all())


async def count_users(session: AsyncSession) -> int:
    result = await session.execute(select(func.count()).select_from(User))
    return result.scalar_one()


async def update_user(
    session: AsyncSession,
    user_id: str,
    **fields: str | bool | None,
) -> User | None:
    user = await get_user_by_id(session, user_id)
    if not user:
        return None
    for key, value in fields.items():
        if value is not None and hasattr(user, key):
            setattr(user, key, value)
    user.updated_at = datetime.now(timezone.utc)
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: str) -> bool:
    user = await get_user_by_id(session, user_id)
    if not user:
        return False
    await session.delete(user)
    await session.flush()
    return True


# --- Class wrapper ---


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, email: str, name: str, hashed_password: str, role: str = "user"
    ) -> User:
        return await create_user(self.session, email, name, hashed_password, role)

    async def get_by_id(self, user_id: str) -> User | None:
        return await get_user_by_id(self.session, user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await get_user_by_email(self.session, email)

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[User]:
        return await list_users(self.session, limit, offset)

    async def count(self) -> int:
        return await count_users(self.session)

    async def update(self, user_id: str, **fields: str | bool | None) -> User | None:
        return await update_user(self.session, user_id, **fields)

    async def delete(self, user_id: str) -> bool:
        return await delete_user(self.session, user_id)
