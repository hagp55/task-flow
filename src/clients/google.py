import logging
from dataclasses import dataclass

import requests

from src.apps.auth.schemas import GoogleUserDataOut
from src.core.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class GoogleClient:
    def get_user_info(self, code) -> GoogleUserDataOut:
        access_token: str = self._get_user_access_token(
            code=code,
        )
        response: requests.Response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        google_data = GoogleUserDataOut(
            **response.json(),
            google_access_token=access_token,
        )
        logger.info(google_data)
        return google_data

    def _get_user_access_token(self, code: str) -> str:
        payload: dict[str, str] = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        response: requests.Response = requests.post(
            settings.GOOGLE_TOKEN_URL,
            data=payload,
        )
        return response.json()["access_token"]
