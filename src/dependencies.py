import logging
import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, Security, security
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.auth.services import AuthService
from src.apps.projects.repository import ProjectRepository
from src.apps.projects.services import ProjectService
from src.apps.tasks.cache_repositories import CacheTasks
from src.apps.tasks.repository import TaskRepository
from src.apps.tasks.services import TasksService
from src.apps.users.models import User
from src.apps.users.repositories import UsersRepository
from src.apps.users.services import UsersService
from src.core.db import get_async_session
from src.core.services.cache import get_redis_connection
from src.core.services.clients.google import GoogleClient
from src.core.services.clients.mail import MailClient
from src.core.services.clients.yandex import YandexClient
from src.exceptions import (
    TokenExpiredException,
    TokenHasNotValidSignatureException,
)

logger = logging.getLogger(__name__)
reusable_oauth2 = security.HTTPBearer()


session = Annotated[AsyncSession, Depends(get_async_session)]


def get_mail_client() -> MailClient:
    return MailClient()


def get_google_client() -> GoogleClient:
    return GoogleClient()


def get_yandex_client() -> YandexClient:
    return YandexClient()


def get_tasks_repository(
    session: session,
) -> TaskRepository:
    return TaskRepository(session=session)


def get_cache_tasks_repository() -> CacheTasks:
    redis_connection: Redis = get_redis_connection()  # type: ignore
    return CacheTasks(redis=redis_connection)


def get_users_repository(
    session: session,
) -> UsersRepository:
    return UsersRepository(session=session)


def get_project_repository(
    session: session,
) -> ProjectRepository:
    return ProjectRepository(session=session)


def get_project_service(
    project_repository: Annotated[ProjectRepository, Depends(get_project_repository)],
) -> ProjectService:
    return ProjectService(project_repository=project_repository)


def get_tasks_service(
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
    cache_task_repository: Annotated[CacheTasks, Depends(get_cache_tasks_repository)],
    project_repository: Annotated[ProjectRepository, Depends(get_project_repository)],
) -> TasksService:
    return TasksService(
        task_repository=task_repository,
        project_repository=project_repository,
        cache_task_repository=cache_task_repository,
    )


def get_auth_service(
    users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
    google_client: Annotated[GoogleClient, Depends(get_google_client)],
    yandex_client: Annotated[YandexClient, Depends(get_yandex_client)],
    mail_client: Annotated[MailClient, Depends(get_mail_client)],
) -> AuthService:
    return AuthService(
        users_repository=users_repository,
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=mail_client,
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
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> uuid.UUID:
    try:
        user_id: uuid.UUID = auth_service.get_user_id_from_access_token(access_token=token.credentials)
    except (TokenExpiredException, TokenHasNotValidSignatureException) as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail,
        )
    return user_id


async def get_request_staff_or_superuser_user_id(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> uuid.UUID:
    try:
        user_id: uuid.UUID = auth_service.get_user_id_from_access_token(access_token=token.credentials)
    except (TokenExpiredException, TokenHasNotValidSignatureException) as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail,
        )
    user: User | None = await users_repository.get(user_id=user_id)
    if user:
        if not (user.is_staff or user.is_super_user):
            raise HTTPException(
                status_code=401,
                detail="Permission denied",
            )
    return user_id
