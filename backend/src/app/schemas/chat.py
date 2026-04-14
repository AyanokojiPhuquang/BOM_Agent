from pydantic import BaseModel

from src.app.schemas.conversation import ImageAttachment


class ChatMessage(BaseModel):
    role: str
    content: str
    images: list[ImageAttachment] | None = None


class ChatCompletionRequest(BaseModel):
    model: str = "openai/gpt-5.4-mini"
    messages: list[ChatMessage]
    stream: bool = True
    conversation_id: str | None = None


class ToolCallDelta(BaseModel):
    name: str
    args: dict | None = None


class ToolResultDelta(BaseModel):
    name: str
    content: str


class Delta(BaseModel):
    role: str | None = None
    content: str | None = None
    tool_call: ToolCallDelta | None = None
    tool_result: ToolResultDelta | None = None


class ChoiceDelta(BaseModel):
    index: int = 0
    delta: Delta
    finish_reason: str | None = None


class ChatCompletionChunk(BaseModel):
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: list[ChoiceDelta]
