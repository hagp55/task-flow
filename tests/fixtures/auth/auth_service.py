import pytest

from src.apps.auth.services import AuthService
from src.apps.users.repositories import UsersRepository
from src.core.services.clients.mail import MailClient


@pytest.fixture
def mock_auth_service(google_client, yandex_client, fake_users_repository) -> AuthService:
    return AuthService(
        users_repository=fake_users_repository,
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=MailClient(),
    )


@pytest.fixture
def auth_service(google_client, yandex_client, session) -> AuthService:
    return AuthService(
        users_repository=UsersRepository(session),
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=MailClient(),
    )
