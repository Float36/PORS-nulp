from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.repositories import PhotoRepository
from src.app.schemas.photo import PhotoCreate, PhotoUpdate


class CRUDPhoto:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = PhotoRepository(session)

    async def get_all(self):
        photos = await self.repository.get_all()
        return [self._to_response(item) for item in photos]

    async def get_by_id(self, photo_id: int):
        photo = await self.repository.get_by_id(photo_id)
        return self._to_response(photo) if photo else None

    async def create(self, obj_in: PhotoCreate):
        photo = await self.repository.create(obj_in)
        return self._to_response(photo)

    async def update(self, photo_id: int, obj_in: PhotoUpdate):
        photo = await self.repository.update(photo_id, obj_in)
        return self._to_response(photo) if photo else None

    async def delete(self, photo_id: int) -> bool:
        return await self.repository.delete(photo_id)

    @staticmethod
    def _to_response(photo):
        return {
            "id": photo.id,
            "url": photo.url,
            "ad_id": photo.ad_id,
        }
