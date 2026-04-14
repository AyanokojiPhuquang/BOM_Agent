import asyncio
import random

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from loguru import logger
from starlette.background import BackgroundTask

from src.agents import BomAssistantContext, ainvoke, astream_events
from src.agents.streaming import StreamChunk, StreamToolCall, StreamToolResult
from src.agents.checkpointer import get_checkpointer
from src.app.auth import get_current_user
from src.app.dependencies import get_conversation_repository
from src.app.schemas.chat import ChatCompletionRequest
from src.app.utils.chat_utils import (
    content_chunk,
    make_completion_id,
    role_chunk,
    stop_chunk,
    tool_call_chunk,
    tool_result_chunk,
    unix_timestamp,
)
from src.app.utils.image_utils import save_images
from src.configs import SETTINGS
from src.db.database import get_manual_db_session
from src.db.models.conversations import MessageRole
from src.db.models.users import User
from src.db.repositories.conversation import ConversationRepository

router = APIRouter()

_active_streams: dict[str, bool] = {}

MOCK_RESPONSES = [
    "I'd be happy to help you with that! Let me think about it for a moment. "
    "That's a great question and there are several ways to approach it. "
    "The most important thing is to consider the context and find the best solution for your specific needs.",
    "Thanks for reaching out! I can definitely assist you with this. "
    "Let me break it down step by step so it's easier to follow. "
    "First, let's understand the core concept, then we can explore the practical applications.",
    "That's an interesting point! Here's what I think about it. "
    "There are multiple perspectives to consider, and each has its own merits. "
    "I'd recommend starting with the fundamentals and building from there.",
    "Great question! Let me provide you with a comprehensive answer. "
    "The key insight here is that understanding the underlying principles makes everything else fall into place. "
    "I hope that helps clarify things for you!",
]


def _split_into_chunks(text: str, min_size: int = 2, max_size: int = 5) -> list[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        size = random.randint(min_size, max_size)
        chunks.append(" ".join(words[i : i + size]))
        i += size
    return chunks


async def _persist_message(
    conversation_id: str,
    role: MessageRole,
    content: str,
    images: list | None = None,
    message_type: str | None = None,
    tool_name: str | None = None,
) -> None:
    try:
        async with get_manual_db_session() as session:
            repo = ConversationRepository(session)
            await repo.add_message(
                conversation_id, role, content,
                images=images, message_type=message_type, tool_name=tool_name,
            )
    except Exception:
        logger.opt(exception=True).error(
            "Failed to persist {} message for conversation {}",
            role.value,
            conversation_id,
        )


@router.post("/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    current_user: User = Depends(get_current_user),
    repo: ConversationRepository = Depends(get_conversation_repository),
):
    completion_id = make_completion_id()
    created = unix_timestamp()
    model = request.model

    # Get or create conversation
    conversation_id = request.conversation_id
    if not conversation_id:
        conv = await repo.create(user_id=current_user.id)
        conversation_id = conv.id
        # Commit so the new conversation is visible to _persist_message's separate session
        await repo.session.commit()

    last_msg = request.messages[-1]
    query = last_msg.content
    use_agent = bool(SETTINGS.openai_api_key)

    # Extract and persist images
    image_urls: list[str] | None = None
    db_images: list[dict] | None = None
    if last_msg.images:
        image_urls = [img.dataUrl for img in last_msg.images]
        db_images = [img.model_dump() for img in last_msg.images]
        # Save image files to disk (fire-and-forget persistence)
        save_images(db_images)
        logger.info(f"Received {len(last_msg.images)} image(s) with message")

    if not request.stream:
        # --- Non-streaming ---
        await _persist_message(conversation_id, MessageRole.USER, query, images=db_images)

        if use_agent:
            try:
                context = BomAssistantContext(
                    session_id=completion_id,
                    user_id=current_user.id,
                    user_email=current_user.email,
                    conversation_id=conversation_id,
                )
                checkpointer = await get_checkpointer()
                result = await ainvoke(
                    query=query,
                    context=context,
                    checkpointer=checkpointer,
                    image_urls=image_urls,
                )
                response_text = result["response"]
            except Exception as e:
                logger.error(f"Agent invoke error: {e}")
                response_text = "I'm sorry, I encountered an error. Please try again."
        else:
            response_text = random.choice(MOCK_RESPONSES)

        await _persist_message(conversation_id, MessageRole.ASSISTANT, response_text)
        return {
            "id": completion_id,
            "object": "chat.completion",
            "created": created,
            "model": model,
            "conversation_id": conversation_id,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": response_text},
                    "finish_reason": "stop",
                }
            ],
        }

    # --- Streaming ---
    # Each entry: (content_parts, message_type, tool_name)
    finalized_messages: list[tuple[list[str], str, str | None]] = []
    current_parts: list[str] = []

    async def _sse_gen():
        nonlocal current_parts
        await _persist_message(conversation_id, MessageRole.USER, query, images=db_images)

        yield role_chunk(completion_id, model, created)

        if use_agent:
            try:
                context = BomAssistantContext(
                    session_id=completion_id,
                    user_id=current_user.id,
                    user_email=current_user.email,
                    conversation_id=conversation_id,
                )
                checkpointer = await get_checkpointer()
                async for event in astream_events(
                    query=query,
                    context=context,
                    checkpointer=checkpointer,
                    image_urls=image_urls,
                ):
                    if _active_streams.get(completion_id) is False:
                        break
                    if isinstance(event, StreamChunk):
                        yield content_chunk(completion_id, model, created, event.content)
                        current_parts.append(event.content)
                    elif isinstance(event, StreamToolCall):
                        yield tool_call_chunk(completion_id, model, created, event.name, event.args)
                        # Finalize current segment as a tool_call message
                        finalized_messages.append((current_parts, "tool_call", event.name))
                        current_parts = []
                    elif isinstance(event, StreamToolResult):
                        yield tool_result_chunk(completion_id, model, created, event.name, event.content)
            except Exception as e:
                logger.error(f"Agent stream error: {e}")
                error_msg = "I'm sorry, I encountered an error. Please try again."
                yield content_chunk(completion_id, model, created, error_msg)
                current_parts.append(error_msg)
        else:
            response_text = random.choice(MOCK_RESPONSES)
            chunks = _split_into_chunks(response_text)
            for chunk_text in chunks:
                if _active_streams.get(completion_id) is False:
                    break
                await asyncio.sleep(random.uniform(0.015, 0.04))
                yield content_chunk(completion_id, model, created, chunk_text + " ")
                current_parts.append(chunk_text + " ")

        yield stop_chunk(completion_id, model, created)
        yield "data: [DONE]\n\n"
        _active_streams.pop(completion_id, None)

    async def _persist_after_stream() -> None:
        # Persist tool-call messages
        for parts, msg_type, tool_name in finalized_messages:
            text = "".join(parts)
            await _persist_message(
                conversation_id, MessageRole.ASSISTANT, text,
                message_type=msg_type, tool_name=tool_name,
            )
        # Persist final text message
        final_text = "".join(current_parts)
        if final_text:
            await _persist_message(
                conversation_id, MessageRole.ASSISTANT, final_text,
                message_type="text",
            )

    return StreamingResponse(
        _sse_gen(),
        media_type="text/event-stream",
        background=BackgroundTask(_persist_after_stream),
        headers={"X-Conversation-Id": conversation_id},
    )


@router.post("/chat/completions/{completion_id}/stop")
async def stop_completion(completion_id: str):
    _active_streams[completion_id] = False
    return {"status": "stopped"}
