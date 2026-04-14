from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.models.conversations import Conversation, ConversationMessage, MessageRole
from src.db.models.users import User  # ensure FK metadata is registered


# --- Standalone functions ---


async def create_conversation(
    session: AsyncSession,
    user_id: str,
    title: str | None = None,
) -> Conversation:
    conv = Conversation(user_id=user_id, title=title or "New Chat")
    session.add(conv)
    await session.flush()
    return conv


async def get_conversation_by_id(
    session: AsyncSession,
    conversation_id: str,
    include_messages: bool = False,
) -> Conversation | None:
    stmt = select(Conversation).where(Conversation.id == conversation_id)
    if include_messages:
        stmt = stmt.options(selectinload(Conversation.messages))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def list_conversations_by_user(
    session: AsyncSession,
    user_id: str,
    limit: int = 50,
    offset: int = 0,
) -> list[Conversation]:
    stmt = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def update_conversation_title(
    session: AsyncSession,
    conversation_id: str,
    title: str,
) -> Conversation | None:
    from datetime import datetime, timezone

    stmt = (
        update(Conversation)
        .where(Conversation.id == conversation_id)
        .values(title=title, updated_at=datetime.now(timezone.utc))
    )
    await session.execute(stmt)
    await session.flush()
    return await get_conversation_by_id(session, conversation_id)


async def delete_conversation(session: AsyncSession, conversation_id: str) -> bool:
    await session.execute(
        delete(ConversationMessage).where(
            ConversationMessage.conversation_id == conversation_id
        )
    )
    result = await session.execute(
        delete(Conversation).where(Conversation.id == conversation_id)
    )
    return result.rowcount > 0


async def add_message(
    session: AsyncSession,
    conversation_id: str,
    role: MessageRole,
    content: str,
    images: list | None = None,
    message_type: str | None = None,
    tool_name: str | None = None,
) -> ConversationMessage:
    msg = ConversationMessage(
        conversation_id=conversation_id,
        role=role,
        content=content,
        images=images,
        message_type=message_type,
        tool_name=tool_name,
    )
    session.add(msg)

    from datetime import datetime, timezone

    stmt = (
        update(Conversation)
        .where(Conversation.id == conversation_id)
        .values(updated_at=datetime.now(timezone.utc))
    )
    await session.execute(stmt)
    await session.flush()
    return msg


async def get_messages(
    session: AsyncSession,
    conversation_id: str,
) -> list[ConversationMessage]:
    stmt = (
        select(ConversationMessage)
        .where(ConversationMessage.conversation_id == conversation_id)
        .order_by(ConversationMessage.created_at.asc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


# --- Class wrapper ---


class ConversationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: str, title: str | None = None) -> Conversation:
        return await create_conversation(self.session, user_id, title)

    async def get_by_id(
        self, conversation_id: str, include_messages: bool = False
    ) -> Conversation | None:
        return await get_conversation_by_id(
            self.session, conversation_id, include_messages
        )

    async def list_by_user(
        self, user_id: str, limit: int = 50, offset: int = 0
    ) -> list[Conversation]:
        return await list_conversations_by_user(
            self.session, user_id, limit, offset
        )

    async def update_title(self, conversation_id: str, title: str) -> Conversation | None:
        return await update_conversation_title(self.session, conversation_id, title)

    async def delete(self, conversation_id: str) -> bool:
        return await delete_conversation(self.session, conversation_id)

    async def add_message(
        self,
        conversation_id: str,
        role: MessageRole,
        content: str,
        images: list | None = None,
        message_type: str | None = None,
        tool_name: str | None = None,
    ) -> ConversationMessage:
        return await add_message(
            self.session, conversation_id, role, content, images,
            message_type=message_type, tool_name=tool_name,
        )

    async def get_messages(self, conversation_id: str) -> list[ConversationMessage]:
        return await get_messages(self.session, conversation_id)
