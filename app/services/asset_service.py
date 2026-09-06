from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.repositories.asset_repository import AssetRepository
from app.schemas.asset import AssetCreate, AssetUpdate
from app.core.exceptions import AssetNotFoundError

class AssetService:

    @staticmethod
    def get_assets(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        symbol: str | None = None,
    ) -> list[Asset]:
        return AssetRepository.get_all(
            db,
            skip=skip,
            limit=limit,
            symbol=symbol,
        )

    @staticmethod
    def get_asset(
        asset_id: int,
        db: Session,
    ) -> Asset | None:
        asset = AssetRepository.get_by_id(asset_id, db)

        if asset is None:
            raise AssetNotFoundError()

        return asset

    @staticmethod
    def create_asset(
        asset: AssetCreate,
        db: Session,
    ) -> Asset:
        return AssetRepository.create(asset, db)

    @staticmethod
    def update_asset(
        asset_id: int,
        asset_data: AssetUpdate,
        db: Session,
    ) -> Asset:
        asset = AssetRepository.get_by_id(asset_id, db)

        if asset is None:
            raise AssetNotFoundError()

        return AssetRepository.update(
            asset,
            asset_data,
            db,
        )

    @staticmethod
    def delete_asset(
        asset_id: int,
        db: Session,
    ) -> None:
        asset = AssetRepository.get_by_id(asset_id, db)

        if asset is None:
            raise AssetNotFoundError()

        AssetRepository.delete(asset, db)