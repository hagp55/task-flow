from typing import Annotated

from fastapi import Depends
from redis import Redis

from src.apps.tasks.cache_repositories import CacheTasks
from src.apps.tasks.repositories import TaskRepository
from src.apps.tasks.services import TasksService
from src.core.db import session_factory
from src.core.services.cache import get_redis_connection


def get_tasks_repository() -> TaskRepository:
    return TaskRepository(session_factory)


def get_cache_tasks_repository() -> CacheTasks:
    redis_connection: Redis = get_redis_connection()
    return CacheTasks(redis_connection)


def get_tasks_service(
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
    cache_task_repository: Annotated[CacheTasks, Depends(get_cache_tasks_repository)],
) -> TasksService:
    return TasksService(task_repository, cache_task_repository)
