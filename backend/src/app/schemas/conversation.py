from pydantic import BaseModel


class ImageAttachment(BaseModel):
    id: str
    dataUrl: str
    name: str
    size: int


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    type: str | None = None
    toolName: str | None = None
    images: list[ImageAttachment] | None = None
    createdAt: int


class ConversationResponse(BaseModel):
    id: str
    title: str
    messages: list[MessageResponse]
    createdAt: int
    updatedAt: int


class ConversationSummary(BaseModel):
    id: str
    title: str
    createdAt: int
    updatedAt: int


class ConversationListResponse(BaseModel):
    items: list[ConversationSummary]


class UpdateTitleRequest(BaseModel):
    title: str
