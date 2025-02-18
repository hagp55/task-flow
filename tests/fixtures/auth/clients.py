from dataclasses import dataclass

import pytest
from faker import Factory as FakerFactory

from src.apps.auth.schemas import GoogleUserDataOut
from tests.fixtures.users.user_model import EXISTS_GOOGLE_EMAIL, EXISTS_GOOGLE_USER_ID

faker = FakerFactory.create()


@dataclass
class FakeGoogleClient:
    async def get_user_info(self, code) -> GoogleUserDataOut:
        access_token: str = await self._get_user_access_token(
            code=code,
        )
        return google_user_info_data()

    async def _get_user_access_token(self, code: str) -> str:
        return f"some fake access token {code}."


@dataclass
class FakeYandexClient:
    async def get_user_info(self, code) -> dict:
        access_token: str = await self._get_user_access_token(
            code=code,
        )
        return {"fake_access_token": access_token}

    async def _get_user_access_token(self, code: str) -> str:
        return f"some fake access token {code}."


@pytest.fixture
def google_client() -> FakeGoogleClient:
    return FakeGoogleClient()


@pytest.fixture
def yandex_client() -> FakeYandexClient:
    return FakeYandexClient()


def google_user_info_data() -> GoogleUserDataOut:
    return GoogleUserDataOut(
        id=EXISTS_GOOGLE_USER_ID,
        email=EXISTS_GOOGLE_EMAIL,
        name=faker.name(),  # type: ignore
        google_access_token=faker.sha256(),
    )
