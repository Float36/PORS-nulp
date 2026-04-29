from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.database import get_db_session
from src.app.crud.crud_users import CRUDUsers
from src.app.schemas.user import UserCreate, UserListResponse, UserResponse, UserUpdate


router = APIRouter(prefix="/users")


@router.get("/", response_model=UserListResponse)
async def list_users(
    session: AsyncSession = Depends(get_db_session),
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    role: Annotated[str | None, Query(max_length=20, description="Exact match on role")] = None,
    is_verified: Annotated[bool | None, Query(description="Filter by verification flag")] = None,
    sort_by: Annotated[Literal["user_id", "email", "role"], Query()] = "user_id",
    sort_order: Annotated[Literal["asc", "desc"], Query()] = "asc",
):
    """List users with pagination, optional filters, and sorting."""
    user_service = CRUDUsers(session)
    return await user_service.list_users(
        skip=skip,
        limit=limit,
        role=role,
        is_verified=is_verified,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get user by id"""
    user_service = CRUDUsers(session)
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, session: AsyncSession = Depends(get_db_session)):
    """Create new user"""
    user_service = CRUDUsers(session)
    return await user_service.create(user_in)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_in: UserUpdate, session: AsyncSession = Depends(get_db_session)):
    """Update existing user"""
    user_service = CRUDUsers(session)
    user = await user_service.update(user_id, user_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_db_session)):
    """Delete user by id"""
    user_service = CRUDUsers(session)
    deleted = await user_service.delete(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )