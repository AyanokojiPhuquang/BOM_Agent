from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from src.app.auth import get_current_user
from src.app.dependencies import get_conversation_repository
from src.app.schemas.conversation import (
    ConversationListResponse,
    ConversationResponse,
    ConversationSummary,
    MessageResponse,
    UpdateTitleRequest,
)
from src.db.models.users import User
from src.db.repositories.conversation import ConversationRepository

router = APIRouter()


def _to_epoch_ms(dt) -> int:
    return int(dt.timestamp() * 1000)


def _msg_to_response(msg) -> MessageResponse:
    return MessageResponse(
        id=msg.id,
        role=msg.role.value if hasattr(msg.role, "value") else msg.role,
        content=msg.content,
        type=getattr(msg, "message_type", None),
        toolName=getattr(msg, "tool_name", None),
        images=msg.images,
        createdAt=_to_epoch_ms(msg.created_at),
    )


def _conv_to_response(conv) -> ConversationResponse:
    messages = [_msg_to_response(m) for m in (conv.messages or [])]
    return ConversationResponse(
        id=conv.id,
        title=conv.title or "New Chat",
        messages=messages,
        createdAt=_to_epoch_ms(conv.created_at),
        updatedAt=_to_epoch_ms(conv.updated_at),
    )


def _conv_to_summary(conv) -> ConversationSummary:
    return ConversationSummary(
        id=conv.id,
        title=conv.title or "New Chat",
        createdAt=_to_epoch_ms(conv.created_at),
        updatedAt=_to_epoch_ms(conv.updated_at),
    )


@router.get("/conversations", response_model=ConversationListResponse)
async def list_conversations(
    current_user: User = Depends(get_current_user),
    repo: ConversationRepository = Depends(get_conversation_repository),
):
    convs = await repo.list_by_user(current_user.id)
    return ConversationListResponse(items=[_conv_to_summary(c) for c in convs])


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    current_user: User = Depends(get_current_user),
    repo: ConversationRepository = Depends(get_conversation_repository),
):
    try:
        conv = await repo.create(user_id=current_user.id)
        conv = await repo.get_by_id(conv.id, include_messages=True)
        return _conv_to_response(conv)
    except Exception as e:
        logger.error(f"Create conversation error: {e}", exc_info=True)
        raise


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    repo: ConversationRepository = Depends(get_conversation_repository),
):
    conv = await repo.get_by_id(conversation_id, include_messages=True)
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return _conv_to_response(conv)


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    repo: ConversationRepository = Depends(get_conversation_repository),
):
    conv = await repo.get_by_id(conversation_id)
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    await repo.delete(conversation_id)


@router.put("/conversations/{conversation_id}/title", response_model=ConversationResponse)
async def update_conversation_title(
    conversation_id: str,
    request: UpdateTitleRequest,
    current_user: User = Depends(get_current_user),
    repo: ConversationRepository = Depends(get_conversation_repository),
):
    conv = await repo.get_by_id(conversation_id, include_messages=True)
    if not conv or conv.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    updated = await repo.update_title(conversation_id, request.title)
    return _conv_to_response(updated)
