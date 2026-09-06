from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.asset import AssetCreate, AssetResponse, AssetUpdate
from app.services.asset_service import AssetService

router = APIRouter(
    prefix="/assets",
    tags=["Assets"],
)

@router.get("", response_model=list[AssetResponse])
def get_assets(
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    symbol: Annotated[
        str | None,
        Query(min_length=1, max_length=20),
    ] = None,
):
    if symbol is not None:
        symbol = symbol.strip().upper()
    return AssetService.get_assets(
        db,
        skip=skip,
        limit=limit,
        symbol=symbol,
    )

@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(
    asset_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    return AssetService.get_asset(asset_id, db)

@router.post("", response_model=AssetResponse)
def create_asset(
    asset: AssetCreate,
    db: Annotated[Session, Depends(get_db)],
):
    return AssetService.create_asset(asset, db)

@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: int,
    asset_data: AssetUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    return AssetService.update_asset(
        asset_id,
        asset_data,
        db,
    )

@router.delete("/{asset_id}", status_code=204)
def delete_asset(
    asset_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    AssetService.delete_asset(asset_id, db)