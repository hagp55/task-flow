import asyncio
import logging
from contextlib import asynccontextmanager

import uvloop
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.apps import api_router
from src.apps.auth.admin import init_admin
from src.core.description import DESCRIPTION, TITLE
from src.core.loggers import set_logging

# from src.core.services.sentry import sentry_init
from src.core.settings import settings
from src.middlewares.corse_middleware import init_corse_middleware

logger = logging.getLogger(__name__)


def _init_loggers(app: FastAPI) -> None:
    set_logging()
    # sentry_init()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await make_amqp_consumer()
    yield


def _init_routers(app: FastAPI) -> None:
    app.include_router(api_router)


def _init_middlewares(app: FastAPI) -> None:
    init_corse_middleware(app)


def _init_admin(_app: FastAPI) -> None:
    init_admin(_app)


def create_app() -> FastAPI:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    _app: FastAPI = FastAPI(
        debug=settings.DEBUG,
        lifespan=lifespan,
        title=TITLE,
        description=DESCRIPTION,
        version=settings.API_VERSION,
        default_response_class=ORJSONResponse,
    )
    _init_loggers(_app)
    _init_middlewares(_app)
    _init_routers(_app)
    _init_admin(_app)
    return _app


app: FastAPI = create_app()
