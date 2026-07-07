from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class CreateChatRequest(BaseModel):
    user_id: int
    title: str = Field(min_length=1, max_length=255)

class SendMessageRequest(BaseModel):
    content: str = Field(min_length=1)

class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chat_session_id: int
    sent_message: str
    received_message: str
    created_at: datetime

class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    created_at: datetime
    messages: list[MessageResponse] = Field(default_factory=list)


class ChatDetailResponse(ChatResponse):
    messages: list[MessageResponse] = Field(default_factory=list)
