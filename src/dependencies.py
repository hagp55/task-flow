import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request, Security, security
from redis import Redis
from sqlalchemy.orm import Session

from src.apps.auth.services import AuthService
from src.apps.tasks.cache_repositories import CacheTasks
from src.apps.tasks.repositories import TaskRepository
from src.apps.tasks.services import TasksService
from src.apps.users.repositories import UsersRepository
from src.apps.users.services import UsersService
from src.clients.google import GoogleClient
from src.clients.yandex import YandexClient
from src.core.db import get_session, session_factory
from src.core.services.cache import get_redis_connection
from src.exceptions import TokenExpiredException, TokenHasNotValidSignatureException

logger = logging.getLogger(__name__)
reusable_oauth2 = security.HTTPBearer()


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


def get_google_client() -> GoogleClient:
    return GoogleClient()


def get_yandex_client() -> YandexClient:
    return YandexClient()


def get_auth_service(
    users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
    google_client: Annotated[GoogleClient, Depends(get_google_client)],
    yandex_client: Annotated[YandexClient, Depends(get_yandex_client)],
) -> AuthService:
    return AuthService(
        users_repository=users_repository,
        google_client=google_client,
        yandex_client=yandex_client,
    )


def get_users_service(
    users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UsersService:
    return UsersService(
        users_repository=users_repository,
        auth_service=auth_service,
    )


async def get_request_user_id(
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> int:
    try:
        user_id: int = auth_service.get_user_id_from_access_token(token.credentials)
    except (TokenExpiredException, TokenHasNotValidSignatureException) as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail,
        )
    return user_id
