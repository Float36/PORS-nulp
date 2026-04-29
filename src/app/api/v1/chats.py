from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.database import get_db_session
from src.app.crud.crud_chats import CRUDChat
from src.app.schemas.chat import ChatCreate, ChatResponse
from src.app.schemas.message import MessageCreateInChat, MessageResponse

router = APIRouter(prefix="/chats")

@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(chat_in: ChatCreate, session: AsyncSession = Depends(get_db_session)):
    """Create a new chat between the initiator and the ad owner"""
    chat_service = CRUDChat(session)
    return await chat_service.create_chat(chat_in.ad_id, chat_in.initiator_id)

@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat_history(chat_id: int, session: AsyncSession = Depends(get_db_session)):
    """View chat history"""
    chat_service = CRUDChat(session)
    chat = await chat_service.get_chat_history(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.post("/{chat_id}/messages", response_model=MessageResponse)
async def send_message(chat_id: int, message_in: MessageCreateInChat, session: AsyncSession = Depends(get_db_session)):
    """Send a message to an existing chat"""
    chat_service = CRUDChat(session)
    return await chat_service.add_message(chat_id, message_in.sender_id, message_in.content)


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: int, session: AsyncSession = Depends(get_db_session)):
    """Delete chat by id"""
    chat_service = CRUDChat(session)
    deleted = await chat_service.delete_chat(chat_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Chat not found")