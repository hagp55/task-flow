from fastapi import APIRouter

from src.apps.healthcheck.schemas import HealthCheckResponseSchema

__all__ = ("router",)


router = APIRouter(prefix="/healthcheck", tags=["Healthcheck"])


@router.get(
    "",
    description="Application status",
    response_model=HealthCheckResponseSchema,
)
async def get_healthcheck_status() -> HealthCheckResponseSchema:
    return HealthCheckResponseSchema()
