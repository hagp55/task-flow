import pytest

from src.apps.auth.services import AuthService
from src.apps.users.repositories import UsersRepository


@pytest.fixture
def mock_auth_service(google_client, yandex_client, fake_users_repository) -> AuthService:
    return AuthService(
        users_repository=fake_users_repository,
        google_client=google_client,
        yandex_client=yandex_client,
    )


@pytest.fixture
def auth_service(google_client, yandex_client, db_session) -> AuthService:
    return AuthService(
        users_repository=UsersRepository(db_session),
        google_client=google_client,
        yandex_client=yandex_client,
    )
