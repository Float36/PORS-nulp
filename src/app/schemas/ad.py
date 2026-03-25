from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PhotoResponse(BaseModel):
    id: int
    url: str

class EmbeddingResponse(BaseModel):
    id: int
    vector: List[float]


class AdBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    location: str
    status: bool = True     # True - found

class AdCreate(AdBase):
    user_id: int
    category_id: int

class AdResponse(AdBase):
    id: int
    user_id: int
    category_id: int
    created_at: datetime
    photos: List[PhotoResponse] = []
    embedding: Optional[EmbeddingResponse] = None

    class Config:
        from_attributes = True