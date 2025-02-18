from dataclasses import dataclass

import pytest

from tests.fixtures.users.user_model import UserFactory


@dataclass
class FakeUsersRepository:
    async def get_user_by_email(self, email: str) -> None:
        return

    async def create(
        self,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        google_access_token: str | None = None,
        yandex_access_token: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ):
        return UserFactory()


@pytest.fixture
def users_repository() -> FakeUsersRepository:
    return FakeUsersRepository()
