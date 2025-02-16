import logging
from dataclasses import dataclass

import httpx

from src.apps.auth.schemas import YandexUserDataOut
from src.core.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class YandexClient:
    async def get_user_info(self, code) -> YandexUserDataOut:
        access_token: str = await self._get_user_access_token(
            code=code,
        )
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.get(
                "https://login.yandex.ru/info?format=json",
                headers={
                    "Authorization": f"OAuth {access_token}",
                },
            )
            return YandexUserDataOut(
                **response.json(),
                access_token=access_token,
            )

    async def _get_user_access_token(self, code: str) -> str:
        payload: dict[str, str] = {
            "code": code,
            "client_id": settings.YANDEX_CLIENT_ID,
            "client_secret": settings.YANDEX_CLIENT_SECRET,
            "grant_type": "authorization_code",
        }
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.post(
                settings.YANDEX_TOKEN_URL,
                data=payload,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            return response.json()["access_token"]
