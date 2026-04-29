from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = None


class CategoryCreate(CategoryBase):
    ad_id: int


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    description: str | None = None
    ad_id: int | None = None


class CategoryResponse(CategoryBase):
    id: int
    ad_id: int
