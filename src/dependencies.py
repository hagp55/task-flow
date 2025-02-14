from typing import Annotated

from fastapi import Depends
from redis import Redis
from sqlalchemy.orm import Session

from src.apps.auth.services import AuthService
from src.apps.tasks.cache_repositories import CacheTasks
from src.apps.tasks.repositories import TaskRepository
from src.apps.tasks.services import TasksService
from src.apps.users.repositories import UsersRepository
from src.apps.users.services import UsersService
from src.core.db import get_session, session_factory
from src.core.services.cache import get_redis_connection


def get_tasks_repository() -> TaskRepository:
    return TaskRepository(session_factory)


# def get_tasks_repository(db_session: Annotated[Session, Depends(get_session)]) -> TaskRepository:
#     return TaskRepository(db_session)


def get_cache_tasks_repository() -> CacheTasks:
    redis_connection: Redis = get_redis_connection()
    return CacheTasks(redis_connection)


def get_users_repository(db_session: Annotated[Session, Depends(get_session)]) -> UsersRepository:
    return UsersRepository(db_session=session_factory)


def get_tasks_service(
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
    cache_task_repository: Annotated[CacheTasks, Depends(get_cache_tasks_repository)],
) -> TasksService:
    return TasksService(task_repository, cache_task_repository)


def get_users_service(
    users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
) -> UsersService:
    return UsersService(users_repository=users_repository)


def get_auth_service(
    users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
) -> AuthService:
    return AuthService(users_repository=users_repository)
