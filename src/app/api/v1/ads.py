from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db.database import get_db_session
from src.app.crud.crud_ads import CRUDAd
from src.app.schemas.ad import AdCreate, AdListResponse, AdResponse, AdUpdate


router = APIRouter(prefix="/ads")


@router.get("/", response_model=AdListResponse)
async def list_ads(
    session: AsyncSession = Depends(get_db_session),
    skip: Annotated[int, Query(ge=0, description="Offset for pagination")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Page size")] = 20,
    user_id: Annotated[int | None, Query(description="Filter by owner user id")] = None,
    status: Annotated[bool | None, Query(description="Filter by ad status")] = None,
    location_contains: Annotated[
        str | None, Query(max_length=255, description="Case-insensitive substring match on location")
    ] = None,
    sort_by: Annotated[
        Literal["created_at", "title", "ad_id"], Query(description="Sort field")
    ] = "created_at",
    sort_order: Annotated[Literal["asc", "desc"], Query(description="Sort direction")] = "desc",
):
    """List ads with pagination, optional filters, and sorting."""
    ad_service = CRUDAd(session)
    return await ad_service.list_ads(
        skip=skip,
        limit=limit,
        user_id=user_id,
        status=status,
        location_contains=location_contains,
        sort_by=sort_by,
        sort_order=sort_order,
    )

@router.get("/{ad_id}", response_model=AdResponse)
async def get_ad_by_id(ad_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get ad by id"""
    ad_service = CRUDAd(session)
    ad = await ad_service.get_by_id(ad_id)
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ad with ID {ad_id} not found"
        )

    return ad


@router.post("/", response_model=AdResponse, status_code=status.HTTP_201_CREATED)
async def create_new_ad(ad_in: AdCreate, session: AsyncSession = Depends(get_db_session)):
    """Create new ad"""
    ad_service = CRUDAd(session)
    return await ad_service.create(ad_in)


@router.put("/{ad_id}", response_model=AdResponse)
async def update_ad(ad_id: int, ad_in: AdUpdate, session: AsyncSession = Depends(get_db_session)):
    """Update ad by id"""
    ad_service = CRUDAd(session)
    ad = await ad_service.update(ad_id, ad_in)
    if not ad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ad with ID {ad_id} not found"
        )
    return ad


@router.delete("/{ad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ad(ad_id: int, session: AsyncSession = Depends(get_db_session)):
    """Delete ad by id"""
    ad_service = CRUDAd(session)
    deleted = await ad_service.delete(ad_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ad with ID {ad_id} not found"
        )