from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.database import get_db_session
from src.app.crud.crud_categories import CRUDCategory
from src.app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter(prefix="/categories")


@router.get("/", response_model=List[CategoryResponse])
async def get_all_categories(session: AsyncSession = Depends(get_db_session)):
    service = CRUDCategory(session)
    return await service.get_all()


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category_by_id(category_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CRUDCategory(session)
    category = await service.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with ID {category_id} not found")
    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category_in: CategoryCreate, session: AsyncSession = Depends(get_db_session)):
    service = CRUDCategory(session)
    return await service.create(category_in)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category_in: CategoryUpdate, session: AsyncSession = Depends(get_db_session)):
    service = CRUDCategory(session)
    category = await service.update(category_id, category_in)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with ID {category_id} not found")
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CRUDCategory(session)
    deleted = await service.delete(category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with ID {category_id} not found")
