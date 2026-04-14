import json
import time
import uuid

from src.app.schemas.chat import (
    ChatCompletionChunk,
    ChoiceDelta,
    Delta,
    ToolCallDelta,
    ToolResultDelta,
)


def make_completion_id() -> str:
    return f"chatcmpl-{uuid.uuid4().hex[:29]}"


def unix_timestamp() -> int:
    return int(time.time())


def content_chunk(
    completion_id: str,
    model: str,
    created: int,
    text: str,
) -> str:
    chunk = ChatCompletionChunk(
        id=completion_id,
        created=created,
        model=model,
        choices=[
            ChoiceDelta(index=0, delta=Delta(content=text), finish_reason=None)
        ],
    )
    return f"data: {chunk.model_dump_json()}\n\n"


def stop_chunk(
    completion_id: str,
    model: str,
    created: int,
) -> str:
    chunk = ChatCompletionChunk(
        id=completion_id,
        created=created,
        model=model,
        choices=[
            ChoiceDelta(index=0, delta=Delta(), finish_reason="stop")
        ],
    )
    return f"data: {chunk.model_dump_json()}\n\n"


def tool_call_chunk(
    completion_id: str,
    model: str,
    created: int,
    name: str,
    args: dict | None = None,
) -> str:
    chunk = ChatCompletionChunk(
        id=completion_id,
        created=created,
        model=model,
        choices=[
            ChoiceDelta(
                index=0,
                delta=Delta(tool_call=ToolCallDelta(name=name, args=args)),
                finish_reason=None,
            )
        ],
    )
    return f"data: {chunk.model_dump_json()}\n\n"


def tool_result_chunk(
    completion_id: str,
    model: str,
    created: int,
    name: str,
    content: str,
) -> str:
    chunk = ChatCompletionChunk(
        id=completion_id,
        created=created,
        model=model,
        choices=[
            ChoiceDelta(
                index=0,
                delta=Delta(tool_result=ToolResultDelta(name=name, content=content)),
                finish_reason=None,
            )
        ],
    )
    return f"data: {chunk.model_dump_json()}\n\n"


def role_chunk(
    completion_id: str,
    model: str,
    created: int,
) -> str:
    chunk = ChatCompletionChunk(
        id=completion_id,
        created=created,
        model=model,
        choices=[
            ChoiceDelta(index=0, delta=Delta(role="assistant"), finish_reason=None)
        ],
    )
    return f"data: {chunk.model_dump_json()}\n\n"
