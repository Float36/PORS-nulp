from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.schemas.category import CategoryResponse
from app.schemas.photo import PhotoResponse


class AdBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: str | None = None
    location: str
    status: bool = True


class AdCategoryCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = None


class AdCreate(AdBase):
    user_id: int
    categories: List[AdCategoryCreate] = Field(default_factory=list)
    photos: List[str] = Field(default_factory=list)


class AdUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = None
    location: str | None = None
    status: bool | None = None
    categories: List[AdCategoryCreate] | None = None
    photos: List[str] | None = None


class AdResponse(AdBase):
    id: int
    user_id: int
    created_at: datetime
    categories: List[CategoryResponse] = Field(default_factory=list)
    photos: List[PhotoResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class AdListResponse(BaseModel):
    items: List[AdResponse]
    total: int
    skip: int
    limit: int
