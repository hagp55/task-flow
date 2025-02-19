import logging
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from src.apps.auth.schemas import GoogleUserDataOut, YandexUserDataOut
from src.apps.users.models import User
from src.apps.users.repositories import UsersRepository
from src.apps.users.schemas import UserLoginOut
from src.core.services.clients.google import GoogleClient
from src.core.services.clients.mail import MailClient
from src.core.services.clients.yandex import YandexClient
from src.core.settings import settings
from src.exceptions import (
    TokenExpiredException,
    TokenHasNotValidSignatureException,
    UserNotCorrectPasswordException,
    UserNotFoundException,
)

logger = logging.getLogger(__name__)


@dataclass
class AuthService:
    users_repository: UsersRepository
    google_client: GoogleClient
    yandex_client: YandexClient
    mail_client: MailClient

    async def login(self, username: str, password: str) -> UserLoginOut:
        user: User | None = await self.users_repository.get_by_username(
            username=username,
        )
        await self._validate_auth_user(user, password)
        access_token: str = self.generate_access_token(user_id=user.id)
        return UserLoginOut(id=user.id, access_token=access_token)

    def get_google_redirect_url(self) -> str:
        return settings.GOOGLE_REDIRECT_URL

    async def google_auth(self, code: str) -> UserLoginOut:
        user_data: GoogleUserDataOut = await self.google_client.get_user_info(code)
        if user := await self.users_repository.get_user_by_email(
            email=user_data.email,
        ):
            return UserLoginOut(
                id=user.id,
                access_token=self.generate_access_token(user.id),
            )
        user: User | None = await self.users_repository.create(
            email=user_data.email,
            first_name=user_data.name,
            google_access_token=user_data.google_access_token,
        )
        self.mail_client.send_welcome_email(to=user_data.email)
        return UserLoginOut(
            id=user.id,
            access_token=self.generate_access_token(user.id),
        )

    def get_yandex_redirect_url(self) -> str:
        return settings.YANDEX_REDIRECT_URL

    async def yandex_auth(self, code: str) -> UserLoginOut:
        user_data: YandexUserDataOut = await self.yandex_client.get_user_info(code)
        if user := await self.users_repository.get_user_by_email(
            email=user_data.email,
        ):
            return UserLoginOut(
                id=user.id,
                access_token=self.generate_access_token(user.id),
            )
        user: User | None = await self.users_repository.create(
            email=user_data.email,
            first_name=user_data.name,
            yandex_access_token=user_data.access_token,
        )
        self.mail_client.send_welcome_email(to=user_data.email)
        return UserLoginOut(
            id=user.id,
            access_token=self.generate_access_token(user.id),
        )

    @staticmethod
    async def _validate_auth_user(user: User, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    @staticmethod
    def generate_access_token(user_id: int) -> str:
        expires_date: datetime = datetime.now(UTC) + timedelta(hours=settings.JWT_UPDATE_TIME)
        payload: dict[str, Any] = {
            "id": user_id,
            "expire": int(expires_date.timestamp()),
        }
        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            settings.JWT_ALGORITHM,
        )

    @staticmethod
    def get_user_id_from_access_token(access_token: str) -> int:
        try:
            payload: dict[str, Any] = jwt.decode(
                access_token,
                settings.JWT_SECRET_KEY,
                algorithms=[
                    settings.JWT_ALGORITHM,
                ],
            )
        except JWTError:
            raise TokenHasNotValidSignatureException
        if payload["expire"] < datetime.now(UTC).timestamp():
            raise TokenExpiredException
        return payload["id"]
