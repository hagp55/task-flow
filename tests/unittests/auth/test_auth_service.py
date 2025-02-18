from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt

from src.apps.auth.services import AuthService
from src.apps.users.models import User
from src.apps.users.schemas import UserLoginOut
from src.core.settings import settings


def test_get_google_redirect_utr__success(
    mock_auth_service: AuthService,
) -> None:
    from_settings_google_redirect_url: str = settings.GOOGLE_REDIRECT_URL
    auth_service_google_redirect_url: str = mock_auth_service.get_google_redirect_url()

    assert from_settings_google_redirect_url == auth_service_google_redirect_url


def test_get_google_redirect_utr__fail(
    mock_auth_service: AuthService,
) -> None:
    from_settings_google_redirect_url: str = "https://fake_google_redirect_url.com"
    auth_service_google_redirect_url: str = mock_auth_service.get_google_redirect_url()

    assert from_settings_google_redirect_url != auth_service_google_redirect_url


def test_get_yandex_redirect_utr__success(
    mock_auth_service: AuthService,
) -> None:
    from_settings_yandex_redirect_url: str = settings.YANDEX_REDIRECT_URL
    auth_service_yandex_redirect_url: str = mock_auth_service.get_yandex_redirect_url()

    assert from_settings_yandex_redirect_url == auth_service_yandex_redirect_url


def test_get_yandex_redirect_utr__fail(
    mock_auth_service: AuthService,
) -> None:
    from_settings_yandex_redirect_url: str = "https://fake_yandex_redirect_url.com"
    auth_service_yandex_redirect_url: str = mock_auth_service.get_yandex_redirect_url()

    assert from_settings_yandex_redirect_url != auth_service_yandex_redirect_url


def test_generate_access_token__success(
    mock_auth_service: AuthService,
) -> None:
    user_id = 1
    access_token: str = mock_auth_service.generate_access_token(user_id)
    decoded_access_token: dict[str, Any] = jwt.decode(
        access_token,
        settings.JWT_SECRET_KEY,
        algorithms=[
            settings.JWT_ALGORITHM,
        ],
    )
    decoded_user_id: int = decoded_access_token["id"]
    decoded_token_expire: datetime = datetime.fromtimestamp(decoded_access_token["expire"], tz=UTC)

    assert isinstance(access_token, str)
    assert decoded_user_id == user_id
    assert (decoded_token_expire - datetime.now(UTC)) > (
        timedelta(hours=settings.JWT_UPDATE_TIME) - timedelta(seconds=5)
    )


def test_get_user_if_from_access_token__success(
    mock_auth_service: AuthService,
) -> None:
    user_id = 1
    access_token: str = mock_auth_service.generate_access_token(user_id)
    decoded_user_id: int = mock_auth_service.get_user_id_from_access_token(access_token)

    assert decoded_user_id == user_id


async def test_google_auth__success(mock_auth_service: AuthService, user: User) -> None:
    user_data: UserLoginOut = await mock_auth_service.google_auth(code="fake_code")
    # decoded_user_id: int = auth_service.get_user_id_from_access_token(user.google_access_token)  # FIX IT

    assert isinstance(user_data, UserLoginOut)
    # assert decoded_user_id == user_data.id
