from fastapi import APIRouter, HTTPException, status
from src.app.schemas.chat import ChatResponse, MessageResponse
from src.app.crud.crud_chats import chat_service

router = APIRouter(prefix="/chats")

@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat(ad_id: int, initiator_id: int):
    """Create a new chat between the initiator and the ad owner"""
    return chat_service.create_chat(ad_id, initiator_id)

@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat_history(chat_id: int):
    """View chat history"""
    chat = chat_service.get_chat_history(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.post("/{chat_id}/messages", response_model=MessageResponse)
def send_message(chat_id: int, sender_id: int, content: str):
    """Send a message to an existing chat"""
    return chat_service.add_message(chat_id, sender_id, content)