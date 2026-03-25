from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class MessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000, description="Message text")

class MessageCreate(MessageBase):
    sender_id: int

class MessageResponse(MessageBase):
    id: int
    sender_id: int
    timestamp: datetime

    class Config:
        from_attributes = True



class ChatBase(BaseModel):
    ad_id: int
    initiator_id: int

class ChatCreate(ChatBase):
    pass

class ChatResponse(ChatBase):
    id: int
    created_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True