from fastapi import APIRouter, HTTPException, status
from typing import List
from src.app.schemas.ad import AdCreate, AdResponse
from src.app.crud.crud_ads import ad_service


router = APIRouter(prefix="/ads")

@router.get("/", response_model=List[AdResponse])
def get_all_ads():
    """Get list of all ads"""
    return ad_service.get_all()

@router.get("/{ad_id}", response_model=AdResponse)
def get_add_by_id(ad_id: int):
    """Get add by id"""
    ad = ad_service.get_by_id(ad_id)
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ad with ID {ad_id} not found"
        )

    return ad


@router.post("/", response_model=AdResponse, status_code=status.HTTP_201_CREATED)
def create_new_ad(ad_in: AdCreate):
    """Create new ad"""
    return ad_service.create(ad_in)