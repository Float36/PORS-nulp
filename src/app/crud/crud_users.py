from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.repositories import UserRepository
from src.app.schemas.user import UserCreate, UserUpdate


class CRUDUsers:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = UserRepository(session)

    async def get_all(self):
        users = await self.repository.get_all()
        return [self._to_response(user) for user in users]

    async def list_users(
        self,
        *,
        skip: int,
        limit: int,
        role: str | None,
        is_verified: bool | None,
        sort_by: str,
        sort_order: str,
    ) -> dict:
        users, total = await self.repository.list_users(
            skip=skip,
            limit=limit,
            role=role,
            is_verified=is_verified,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return {
            "items": [self._to_response(user) for user in users],
            "total": total,
            "skip": skip,
            "limit": limit,
        }

    async def get_by_id(self, user_id: int):
        user = await self.repository.get_by_id(user_id)
        if not user:
            return None
        return self._to_response(user)

    async def create(self, obj_in: UserCreate):
        user = await self.repository.create(obj_in)
        return self._to_response(user)

    async def update(self, user_id: int, obj_in: UserUpdate):
        user = await self.repository.update(user_id, obj_in)
        return self._to_response(user) if user else None

    async def delete(self, user_id: int) -> bool:
        return await self.repository.delete(user_id)

    @staticmethod
    def _to_response(user):
        return {
            "id": user.user_id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_verified": user.is_verified,
        }