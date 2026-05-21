from datetime import datetime

from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000, description="Message text")


class MessageCreate(MessageBase):
    chat_id: int
    sender_id: int


class MessageCreateInChat(MessageBase):
    sender_id: int


class MessageUpdate(BaseModel):
    content: str | None = Field(default=None, min_length=1, max_length=1000, description="Message text")
    chat_id: int | None = None
    sender_id: int | None = None


class MessageResponse(MessageBase):
    id: int
    chat_id: int
    sender_id: int | None
    timestamp: datetime

    class Config:
        from_attributes = True
