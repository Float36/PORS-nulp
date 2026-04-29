from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.database import get_db_session
from src.app.crud.crud_photos import CRUDPhoto
from src.app.schemas.photo import PhotoCreate, PhotoResponse, PhotoUpdate

router = APIRouter(prefix="/photos")


@router.get("/", response_model=List[PhotoResponse])
async def get_all_photos(session: AsyncSession = Depends(get_db_session)):
    service = CRUDPhoto(session)
    return await service.get_all()


@router.get("/{photo_id}", response_model=PhotoResponse)
async def get_photo_by_id(photo_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CRUDPhoto(session)
    photo = await service.get_by_id(photo_id)
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Photo with ID {photo_id} not found")
    return photo


@router.post("/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
async def create_photo(photo_in: PhotoCreate, session: AsyncSession = Depends(get_db_session)):
    service = CRUDPhoto(session)
    return await service.create(photo_in)


@router.put("/{photo_id}", response_model=PhotoResponse)
async def update_photo(photo_id: int, photo_in: PhotoUpdate, session: AsyncSession = Depends(get_db_session)):
    service = CRUDPhoto(session)
    photo = await service.update(photo_id, photo_in)
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Photo with ID {photo_id} not found")
    return photo


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_photo(photo_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CRUDPhoto(session)
    deleted = await service.delete(photo_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Photo with ID {photo_id} not found")
