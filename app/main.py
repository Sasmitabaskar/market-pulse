from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.routes.assets import router as assets_router
from app.db.dependencies import get_db

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.constants import (
    ASSET_ALREADY_EXISTS_MESSAGE,
    ASSET_NOT_FOUND_MESSAGE,
)
from app.core.exceptions import AssetNotFoundError
from app.core.exceptions import AssetAlreadyExistsError

app = FastAPI(
    title="MarketPulse",
    description="Real-Time Market Intelligence & Analytics Platform",
    version="0.1.0",
)

@app.exception_handler(AssetNotFoundError)
def asset_not_found_handler(
    request: Request,
    exc: AssetNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": ASSET_NOT_FOUND_MESSAGE,
        },
    )

@app.exception_handler(AssetAlreadyExistsError)
def asset_already_exists_handler(
    request: Request,
    exc: AssetAlreadyExistsError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": ASSET_ALREADY_EXISTS_MESSAGE,
        },
    )


app.include_router(assets_router)


@app.get("/")
def root():
    return {
        "application": "MarketPulse",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/health/database")
def database_health(
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(text("SELECT 1"))

    return {
        "database": "healthy",
        "result": result.scalar(),
    }