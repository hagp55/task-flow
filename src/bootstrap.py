import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.apps import api_router
from src.core.loggers import set_logging
from src.core.settings import settings

logger = logging.getLogger(__name__)


def _init_loggers(app) -> None:
    set_logging()


def _init_routers(app) -> None:
    app.include_router(api_router)


def _init_middlewares(app) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            f"http://{settings.APP_HOST}",
            f"http://{settings.APP_HOST}:{settings.APP_PORT}",
            *settings.ALLOW_ORIGINS_URLS,
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    _app: FastAPI = FastAPI(
        debug=settings.DEBUG,
    )
    _init_loggers(_app)
    _init_middlewares(_app)
    _init_routers(_app)
    return _app


app: FastAPI = create_app()
logger.info(app.user_middleware)
