from pydantic import BaseModel, Field


class PhotoBase(BaseModel):
    url: str = Field(..., max_length=2048)


class PhotoCreate(PhotoBase):
    ad_id: int


class PhotoUpdate(BaseModel):
    url: str | None = Field(default=None, max_length=2048)
    ad_id: int | None = None


class PhotoResponse(PhotoBase):
    id: int
    ad_id: int
