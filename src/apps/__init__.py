from fastapi import APIRouter
from src.apps.healthcheck import healthcheck_router
from src.apps.tasks import task_router
from src.apps.users.router import router as user_router
from src.apps.auth.router import router as auth_router




api_router =  APIRouter(prefix='/api')

v1_router = APIRouter(prefix='/v1')
v1_router.include_router(router=healthcheck_router)
v1_router.include_router(router=task_router)
v1_router.include_router(router=user_router)
v1_router.include_router(router=auth_router)

api_router.include_router(v1_router)
