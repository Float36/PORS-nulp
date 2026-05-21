from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.db.models import Ad, Category, Chat, Message, Photo
from app.schemas.ad import AdCreate, AdUpdate
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.chat import ChatResponse
from app.schemas.message import MessageCreate, MessageResponse, MessageUpdate
from app.schemas.photo import PhotoCreate, PhotoUpdate


class AdRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Ad]:
        result = await self.session.execute(
            select(Ad).options(selectinload(Ad.categories), selectinload(Ad.photos))
        )
        return list(result.scalars().all())

    async def list_ads(
        self,
        *,
        skip: int = 0,
        limit: int = 50,
        user_id: int | None = None,
        status: bool | None = None,
        location_contains: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[Ad], int]:
        filters = []
        if user_id is not None:
            filters.append(Ad.user_id == user_id)
        if status is not None:
            filters.append(Ad.status == status)
        if location_contains:
            safe = location_contains.replace("%", r"\%").replace("_", r"\_")
            filters.append(Ad.location.ilike(f"%{safe}%", escape="\\"))

        sort_map = {
            "created_at": Ad.created_at,
            "title": Ad.title,
            "ad_id": Ad.ad_id,
        }
        col = sort_map.get(sort_by, Ad.created_at)
        order = desc(col) if sort_order == "desc" else asc(col)

        count_stmt = select(func.count()).select_from(Ad)
        if filters:
            count_stmt = count_stmt.where(*filters)
        total = int(await self.session.scalar(count_stmt) or 0)

        stmt = select(Ad).options(selectinload(Ad.categories), selectinload(Ad.photos))
        if filters:
            stmt = stmt.where(*filters)
        stmt = stmt.order_by(order).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def get_by_id(self, ad_id: int) -> Ad | None:
        result = await self.session.execute(
            select(Ad)
            .options(selectinload(Ad.categories), selectinload(Ad.photos))
            .where(Ad.ad_id == ad_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: AdCreate) -> Ad:
        ad = Ad(
            title=data.title,
            description=data.description,
            location=data.location,
            status=data.status,
            user_id=data.user_id,
        )
        ad.categories = [Category(name=item.name, description=item.description) for item in data.categories]
        ad.photos = [Photo(url=url) for url in data.photos]
        self.session.add(ad)
        await self.session.commit()
        return await self.get_by_id(ad.ad_id)  # type: ignore[return-value]

    async def update(self, ad_id: int, data: AdUpdate) -> Ad | None:
        ad = await self.get_by_id(ad_id)
        if not ad:
            return None

        payload = data.model_dump(exclude_unset=True)
        categories = payload.pop("categories", None)
        photos = payload.pop("photos", None)

        for field, value in payload.items():
            setattr(ad, field, value)

        if categories is not None:
            ad.categories = [
                Category(name=item["name"], description=item.get("description")) for item in categories
            ]

        if photos is not None:
            ad.photos = [Photo(url=url) for url in photos]

        await self.session.commit()
        return await self.get_by_id(ad_id)

    async def delete(self, ad_id: int) -> bool:
        ad = await self.get_by_id(ad_id)
        if not ad:
            return False
        await self.session.delete(ad)
        await self.session.commit()
        return True


class ChatRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_chat(self, ad_id: int, initiator_id: int | None) -> Chat:
        chat = Chat(ad_id=ad_id, initiator_id=initiator_id)
        self.session.add(chat)
        await self.session.commit()
        await self.session.refresh(chat)
        return chat

    async def add_message(self, chat_id: int, sender_id: int, content: str) -> Message:
        message = Message(chat_id=chat_id, sender_id=sender_id, content=content)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_chat_history(self, chat_id: int) -> ChatResponse | None:
        result = await self.session.execute(
            select(Chat).options(selectinload(Chat.messages)).where(Chat.chat_id == chat_id)
        )
        chat = result.scalar_one_or_none()
        if not chat:
            return None

        return ChatResponse(
            id=chat.chat_id,
            ad_id=chat.ad_id,
            initiator_id=chat.initiator_id,
            created_at=chat.created_at,
            messages=[
                MessageResponse(
                    id=message.msg_id,
                    chat_id=message.chat_id,
                    sender_id=message.sender_id,
                    content=message.content,
                    timestamp=message.timestamp,
                )
                for message in chat.messages
            ],
        )

    async def delete_chat(self, chat_id: int) -> bool:
        chat = await self.session.get(Chat, chat_id)
        if not chat:
            return False
        await self.session.delete(chat)
        await self.session.commit()
        return True


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Category]:
        result = await self.session.execute(select(Category))
        return list(result.scalars().all())

    async def get_by_id(self, category_id: int) -> Category | None:
        return await self.session.get(Category, category_id)

    async def create(self, data: CategoryCreate) -> Category:
        category = Category(name=data.name, description=data.description, ad_id=data.ad_id)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def update(self, category_id: int, data: CategoryUpdate) -> Category | None:
        category = await self.get_by_id(category_id)
        if not category:
            return None
        payload = data.model_dump(exclude_unset=True)
        for field, value in payload.items():
            setattr(category, field, value)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def delete(self, category_id: int) -> bool:
        category = await self.get_by_id(category_id)
        if not category:
            return False
        await self.session.delete(category)
        await self.session.commit()
        return True


class PhotoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Photo]:
        result = await self.session.execute(select(Photo))
        return list(result.scalars().all())

    async def get_by_id(self, photo_id: int) -> Photo | None:
        return await self.session.get(Photo, photo_id)

    async def create(self, data: PhotoCreate) -> Photo:
        photo = Photo(url=data.url, ad_id=data.ad_id)
        self.session.add(photo)
        await self.session.commit()
        await self.session.refresh(photo)
        return photo

    async def update(self, photo_id: int, data: PhotoUpdate) -> Photo | None:
        photo = await self.get_by_id(photo_id)
        if not photo:
            return None
        payload = data.model_dump(exclude_unset=True)
        for field, value in payload.items():
            setattr(photo, field, value)
        await self.session.commit()
        await self.session.refresh(photo)
        return photo

    async def delete(self, photo_id: int) -> bool:
        photo = await self.get_by_id(photo_id)
        if not photo:
            return False
        await self.session.delete(photo)
        await self.session.commit()
        return True


class MessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Message]:
        result = await self.session.execute(select(Message))
        return list(result.scalars().all())

    async def get_by_id(self, message_id: int) -> Message | None:
        return await self.session.get(Message, message_id)

    async def create(self, data: MessageCreate) -> Message:
        message = Message(content=data.content, chat_id=data.chat_id, sender_id=data.sender_id)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def update(self, message_id: int, data: MessageUpdate) -> Message | None:
        message = await self.get_by_id(message_id)
        if not message:
            return None
        payload = data.model_dump(exclude_unset=True)
        for field, value in payload.items():
            setattr(message, field, value)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def delete(self, message_id: int) -> bool:
        message = await self.get_by_id(message_id)
        if not message:
            return False
        await self.session.delete(message)
        await self.session.commit()
        return True
