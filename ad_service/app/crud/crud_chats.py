from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.repositories import ChatRepository
from app.services.user_client import user_service_client


class CRUDChat:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = ChatRepository(session)

    async def create_chat(self, ad_id: int, initiator_id: int | None):
        if initiator_id is not None:
            await user_service_client.ensure_user_exists(initiator_id)
        chat = await self.repository.create_chat(ad_id=ad_id, initiator_id=initiator_id)
        return {
            "id": chat.chat_id,
            "ad_id": chat.ad_id,
            "initiator_id": chat.initiator_id,
            "created_at": chat.created_at,
            "messages": [],
        }

    async def add_message(self, chat_id: int, sender_id: int, content: str):
        await user_service_client.ensure_user_exists(sender_id)
        message = await self.repository.add_message(chat_id=chat_id, sender_id=sender_id, content=content)
        return {
            "id": message.msg_id,
            "chat_id": message.chat_id,
            "sender_id": message.sender_id,
            "content": message.content,
            "timestamp": message.timestamp,
        }

    async def get_chat_history(self, chat_id: int):
        return await self.repository.get_chat_history(chat_id)

    async def delete_chat(self, chat_id: int) -> bool:
        return await self.repository.delete_chat(chat_id)
