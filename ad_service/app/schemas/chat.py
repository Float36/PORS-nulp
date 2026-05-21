from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.message import MessageResponse


class ChatBase(BaseModel):
    ad_id: int
    initiator_id: Optional[int] = None


class ChatCreate(ChatBase):
    pass


class ChatResponse(ChatBase):
    id: int
    created_at: datetime
    messages: list[MessageResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True
