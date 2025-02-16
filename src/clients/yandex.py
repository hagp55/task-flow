import logging
from dataclasses import dataclass

import requests

from src.apps.auth.schemas import YandexUserDataOut
from src.core.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class YandexClient:
    def get_user_info(self, code) -> YandexUserDataOut:
        access_token: str = self._get_user_access_token(
            code=code,
        )
        response: requests.Response = requests.get(
            "https://login.yandex.ru/info?format=json",
            headers={
                "Authorization": f"OAuth {access_token}",
            },
        )
        data2 = response.json()
        logger.info(data2)
        return YandexUserDataOut(
            **response.json(),
            access_token=access_token,
        )

    def _get_user_access_token(self, code: str) -> str:
        payload: dict[str, str] = {
            "code": code,
            "client_id": settings.YANDEX_CLIENT_ID,
            "client_secret": settings.YANDEX_CLIENT_SECRET,
            "grant_type": "authorization_code",
        }
        response: requests.Response = requests.post(
            settings.YANDEX_TOKEN_URL,
            data=payload,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        return response.json()["access_token"]
