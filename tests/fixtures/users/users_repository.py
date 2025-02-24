from dataclasses import dataclass

import pytest

from tests.fixtures.users.user_model import UserFactory


@dataclass
class FakeUsersRepository:
    async def get_user_by_email(self, email: str) -> None:
        return

    async def create(
        self,
        password: str | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ):
        return UserFactory()


@pytest.fixture
def fake_users_repository() -> FakeUsersRepository:
    return FakeUsersRepository()
