import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.apps.users.schemas import UserLoginOut, UserSignUpIn


@pytest.mark.integration
async def test_login__success(
    get_user: UserSignUpIn,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": get_user.email,
            "password": get_user.password,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert UserLoginOut.model_validate(response.json())


@pytest.mark.parametrize(
    "email,password",
    [
        ("user@example.com", "usernotexi"),
        ("user25@example.com", "usernotexisdf"),
    ],
)
@pytest.mark.integration
async def test_login_wrong_payload__fail(
    email: str,
    password: str,
    get_user: UserSignUpIn,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "User not correct password"}


@pytest.mark.parametrize(
    "email,password",
    [
        ("novaliddomain.com", "usernotexi"),
        ("", "usernotexi"),
        (" " * 10, "usernotexi"),
        (None, "usernotexi"),
        (None, None),
        ("valid@domain.com", None),
        ("valid@domain.com", ""),
        ("valid@domain.com", " " * 10),
        ("valid@domain.com", "abc"),
        ("valid@domain.com", "abc" * 100),
    ],
)
@pytest.mark.integration
async def test_login_no_valid_payload__fail(
    email: str,
    password: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
