from typing import Annotated

import sentry_sdk
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.healthcheck.schemas import HealthCheckDBResponseSchema, HealthCheckResponseSchema
from src.core.db import get_async_session

__all__ = ("router",)


router = APIRouter(prefix="/healthcheck", tags=["Healthcheck 👨‍⚕️"])


@router.get(
    "",
    description="Application status",
    name="Get app status 🌡️",
    response_model=HealthCheckResponseSchema,
)
async def get_healthcheck_status() -> HealthCheckResponseSchema:
    return HealthCheckResponseSchema()


@router.get(
    "/db",
    name="Get database status 💊",
    response_model=HealthCheckDBResponseSchema,
)
async def get_healthcheck_status_db(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> HealthCheckDBResponseSchema:
    try:
        await session.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is no available",
        )

    return HealthCheckDBResponseSchema()


@router.get(
    "/sentry-debug",
    name="Send error to the sentry 🤒",
)
async def trigger_error():
    sentry_sdk.capture_message("This a test error")
    division_by_zero = 1 / 0
