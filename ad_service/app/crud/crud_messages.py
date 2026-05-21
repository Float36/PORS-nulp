from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.repositories import MessageRepository
from app.schemas.message import MessageCreate, MessageUpdate
from app.services.user_client import user_service_client


class CRUDMessage:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = MessageRepository(session)

    async def get_all(self):
        messages = await self.repository.get_all()
        return [self._to_response(item) for item in messages]

    async def get_by_id(self, message_id: int):
        message = await self.repository.get_by_id(message_id)
        return self._to_response(message) if message else None

    async def create(self, obj_in: MessageCreate):
        await user_service_client.ensure_user_exists(obj_in.sender_id)
        message = await self.repository.create(obj_in)
        return self._to_response(message)

    async def update(self, message_id: int, obj_in: MessageUpdate):
        message = await self.repository.update(message_id, obj_in)
        return self._to_response(message) if message else None

    async def delete(self, message_id: int) -> bool:
        return await self.repository.delete(message_id)

    @staticmethod
    def _to_response(message):
        return {
            "id": message.msg_id,
            "content": message.content,
            "chat_id": message.chat_id,
            "sender_id": message.sender_id,
            "timestamp": message.timestamp,
        }
