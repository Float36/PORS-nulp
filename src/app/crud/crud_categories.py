from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.repositories import CategoryRepository
from src.app.schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = CategoryRepository(session)

    async def get_all(self):
        categories = await self.repository.get_all()
        return [self._to_response(item) for item in categories]

    async def get_by_id(self, category_id: int):
        category = await self.repository.get_by_id(category_id)
        return self._to_response(category) if category else None

    async def create(self, obj_in: CategoryCreate):
        category = await self.repository.create(obj_in)
        return self._to_response(category)

    async def update(self, category_id: int, obj_in: CategoryUpdate):
        category = await self.repository.update(category_id, obj_in)
        return self._to_response(category) if category else None

    async def delete(self, category_id: int) -> bool:
        return await self.repository.delete(category_id)

    @staticmethod
    def _to_response(category):
        return {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "ad_id": category.ad_id,
        }
