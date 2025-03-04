from typing import Annotated

import sentry_sdk
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.healthcheck.schemas import HealthCheckDBResponseSchema, HealthCheckResponseSchema
from src.core.db import get_async_session
from src.dependencies import get_request_staff_or_superuser_user_id

router = APIRouter(dependencies=[Depends(get_request_staff_or_superuser_user_id)])


@router.get(
    "",
    name="Get app status",
    response_model=HealthCheckResponseSchema,
)
async def get_healthcheck_status() -> HealthCheckResponseSchema:
    """
    Returns the current status of the application (Only staff).

    This endpoint can be used to check if the API is running and responding correctly.

    **Response:**
    - `200 OK`: API is working.
    """
    return HealthCheckResponseSchema()


@router.get(
    "/db",
    name="Get database status",
    response_model=HealthCheckDBResponseSchema,
)
async def get_healthcheck_status_db(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> HealthCheckDBResponseSchema:
    """
    Checks the availability of the database connection (Only staff).

    This endpoint executes a simple query to verify that the database
    is reachable and responding.

    **Response:**
    - `200 OK`: Database is working.
    - `503 Service Unavailable`: Database is not available.
    """
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
    include_in_schema=False,
)
async def trigger_error():
    sentry_sdk.capture_message("This a test error")
    division_by_zero = 1 / 0
