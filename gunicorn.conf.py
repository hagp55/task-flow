from uvicorn.workers import UvicornWorker

from src.core.settings import settings

bind: str = f"{settings.APP_HOST}:{settings.APP_PORT}"
workers = 4
worker_class = UvicornWorker
