from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.models import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[User]:
        result = await self.session.execute(select(User))
        return list(result.scalars().all())

    async def list_users(
        self,
        *,
        skip: int = 0,
        limit: int = 50,
        role: str | None = None,
        is_verified: bool | None = None,
        sort_by: str = "user_id",
        sort_order: str = "asc",
    ) -> tuple[list[User], int]:
        filters = []
        if role is not None:
            filters.append(User.role == role)
        if is_verified is not None:
            filters.append(User.is_verified == is_verified)

        sort_map = {
            "user_id": User.user_id,
            "email": User.email,
            "role": User.role,
        }
        col = sort_map.get(sort_by, User.user_id)
        order = desc(col) if sort_order == "desc" else asc(col)

        count_stmt = select(func.count()).select_from(User)
        if filters:
            count_stmt = count_stmt.where(*filters)
        total = int(await self.session.scalar(count_stmt) or 0)

        stmt = select(User)
        if filters:
            stmt = stmt.where(*filters)
        stmt = stmt.order_by(order).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def create(self, data: UserCreate) -> User:
        user = User(
            email=data.email,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            role=data.role.value,
            is_verified=data.is_verified,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: int, data: UserUpdate) -> User | None:
        user = await self.get_by_id(user_id)
        if not user:
            return None

        payload = data.model_dump(exclude_unset=True)
        if "role" in payload and payload["role"] is not None:
            payload["role"] = payload["role"].value

        for field, value in payload.items():
            setattr(user, field, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
        await self.session.delete(user)
        await self.session.commit()
        return True
