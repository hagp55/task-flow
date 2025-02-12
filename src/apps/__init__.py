from fastapi import APIRouter
from src.apps.healthcheck import healthcheck_router
from src.apps.tasks import task_router



api_router =  APIRouter(prefix='/api')

v1_router = APIRouter(prefix='/v1')
v1_router.include_router(router=healthcheck_router)
v1_router.include_router(router=task_router)

api_router.include_router(v1_router)
