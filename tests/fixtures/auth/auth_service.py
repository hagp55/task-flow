import pytest

from src.apps.auth.services import AuthService


@pytest.fixture
def auth_service(google_client, yandex_client, users_repository):
    return AuthService(
        users_repository=users_repository,
        google_client=google_client,
        yandex_client=yandex_client,
    )
