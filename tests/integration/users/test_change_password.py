import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.apps.users.schemas import UserSignUpIn


@pytest.mark.integration
async def test_change_password__success(
    get_user: UserSignUpIn,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.put(
        "/api/v1/users/change_password",
        json={
            "email": "user@example.com",
            "old_password": "strong_password",
            "new_password": "new_strong_password",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "password was successfully updated"}


@pytest.mark.integration
async def test_change_wrong_password__fail(
    get_user: UserSignUpIn,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.put(
        "/api/v1/users/change_password",
        json={
            "email": "user@example.com",
            "old_password": "strong_password123",
            "new_password": "new_strong_password",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "User not correct password"}


@pytest.mark.integration
async def test_change_password_not_exists_user___fail(
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.put(
        "/api/v1/users/change_password",
        json={
            "email": "user@example.com",
            "old_password": "strong_password",
            "new_password": "new_strong_password",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "User not found"}


@pytest.mark.parametrize(
    "email,old_password,new_password",
    [
        ("novaliddomain.ru", "password", "new_password"),
        (None, "password", "new_password"),
        ("valid@domain.ru", "pass", "password"),
        ("valid@domain.ru", None, "password"),
        ("novaliddomain.ru", "password", " " * 10),
        ("novaliddomain.ru", "password", None),
    ],
)
@pytest.mark.integration
async def test_change_password_no_valid_payload__fail(
    email: str,
    old_password: str,
    new_password: str | None,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.put(
        "/api/v1/users/change_password",
        json={
            "email": email,
            "old_password": old_password,
            "new_password": new_password,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
