from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.repositories import AdRepository
from src.app.schemas.ad import AdCreate, AdUpdate


class CRUDAd:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AdRepository(session)

    async def get_all(self):
        ads = await self.repository.get_all()
        return [self._to_response(ad) for ad in ads]

    async def list_ads(
        self,
        *,
        skip: int,
        limit: int,
        user_id: int | None,
        status: bool | None,
        location_contains: str | None,
        sort_by: str,
        sort_order: str,
    ) -> dict:
        ads, total = await self.repository.list_ads(
            skip=skip,
            limit=limit,
            user_id=user_id,
            status=status,
            location_contains=location_contains,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return {
            "items": [self._to_response(ad) for ad in ads],
            "total": total,
            "skip": skip,
            "limit": limit,
        }

    async def get_by_id(self, ad_id: int):
        ad = await self.repository.get_by_id(ad_id)
        return self._to_response(ad) if ad else None

    async def create(self, obj_in: AdCreate):
        ad = await self.repository.create(obj_in)
        return self._to_response(ad)

    async def update(self, ad_id: int, obj_in: AdUpdate):
        ad = await self.repository.update(ad_id, obj_in)
        return self._to_response(ad) if ad else None

    async def delete(self, ad_id: int) -> bool:
        return await self.repository.delete(ad_id)

    @staticmethod
    def _to_response(ad):
        return {
            "id": ad.ad_id,
            "title": ad.title,
            "description": ad.description,
            "location": ad.location,
            "status": ad.status,
            "user_id": ad.user_id,
            "created_at": ad.created_at,
            "categories": [
                {
                    "id": category.id,
                    "name": category.name,
                    "description": category.description,
                    "ad_id": category.ad_id,
                }
                for category in ad.categories
            ],
            "photos": [{"id": photo.id, "url": photo.url, "ad_id": photo.ad_id} for photo in ad.photos],
        }