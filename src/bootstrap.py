from fastapi import FastAPI

from src.apps import api_router
from src.core.settings import settings


def _init_routers(app) -> None:
    app.include_router(api_router)


def create_app() -> FastAPI:
    _app: FastAPI = FastAPI(
        debug=settings.DEBUG,
    )
    _init_routers(_app)
    return _app


app: FastAPI = create_app()
