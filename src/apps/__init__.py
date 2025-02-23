from fastapi import APIRouter
from src.apps.healthcheck.router import router as healthcheck_router
from src.apps.projects.routers import router as project_router
from src.apps.tasks.router import router as task_router
from src.apps.users.router import router as user_router
from src.apps.auth.router import router as auth_router




api_router =  APIRouter(prefix='/api')

v1_router = APIRouter(prefix='/v1')
v1_router.include_router(router=healthcheck_router, prefix="/healthcheck", tags=["Healthcheck 👨‍⚕️"])
v1_router.include_router(router=project_router, prefix="/projects", tags=['Projects 👨‍💻'])
v1_router.include_router(router=task_router, prefix="/tasks", tags=["Tasks 📆"])
v1_router.include_router(router=user_router, prefix="/users", tags=["Users 👨‍🦱"])
v1_router.include_router(router=auth_router, prefix="/auth", tags=["Auth 🙋‍♂️"])

api_router.include_router(v1_router)
