from fastapi import APIRouter, HTTPException, status
from typing import List
from src.app.schemas.user import UserResponse, UserCreate
from src.app.crud.crud_users import user_service


router = APIRouter(prefix="/users")


@router.get("/", response_model=List[UserResponse])
def get_all_users():
    """Get list of all users"""
    return user_service.get_all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int):
    """Get user by id"""
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    return user


@router.post("/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate):
    """Create new user"""
    return user_service.create(user_in)