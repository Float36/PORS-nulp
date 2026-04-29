from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.database import get_db_session
from src.app.crud.crud_messages import CRUDMessage
from src.app.schemas.message import MessageCreate, MessageResponse, MessageUpdate

router = APIRouter(prefix="/messages")


@router.get("/", response_model=List[MessageResponse])
async def get_all_messages(session: AsyncSession = Depends(get_db_session)):
    service = CRUDMessage(session)
    return await service.get_all()


@router.get("/{message_id}", response_model=MessageResponse)
async def get_message_by_id(message_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CRUDMessage(session)
    message = await service.get_by_id(message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Message with ID {message_id} not found")
    return message


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(message_in: MessageCreate, session: AsyncSession = Depends(get_db_session)):
    service = CRUDMessage(session)
    return await service.create(message_in)


@router.put("/{message_id}", response_model=MessageResponse)
async def update_message(message_id: int, message_in: MessageUpdate, session: AsyncSession = Depends(get_db_session)):
    service = CRUDMessage(session)
    message = await service.update(message_id, message_in)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Message with ID {message_id} not found")
    return message


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(message_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CRUDMessage(session)
    deleted = await service.delete(message_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Message with ID {message_id} not found")
