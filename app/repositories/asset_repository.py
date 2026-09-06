from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import AssetAlreadyExistsError
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


class AssetRepository:

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        symbol: str | None = None,
    ) -> list[Asset]:
        query = db.query(Asset)

        if symbol:
            query = query.filter(Asset.symbol == symbol)

        return (
            query
            .order_by(Asset.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(
        asset: AssetCreate,
        db: Session,
    ) -> Asset:
        db_asset = Asset(
            symbol=asset.symbol,
            name=asset.name,
        )

        db.add(db_asset)

        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise AssetAlreadyExistsError() from exc

        db.refresh(db_asset)

        return db_asset

    @staticmethod
    def get_by_id(
        asset_id: int,
        db: Session,
    ) -> Asset | None:
        return db.query(Asset).filter(Asset.id == asset_id).first()

    @staticmethod
    def update(
        asset: Asset,
        asset_data: AssetUpdate,
        db: Session,
    ) -> Asset:
        asset.symbol = asset_data.symbol
        asset.name = asset_data.name

        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise AssetAlreadyExistsError() from exc

        db.refresh(asset)

        return asset

    @staticmethod
    def delete(
        asset: Asset,
        db: Session,
    ) -> None:
        db.delete(asset)
        db.commit()