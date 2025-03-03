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
            "email": get_user.email,
            "old_password": get_user.password,
            "new_password": f"new_{get_user.password}",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "password was successfully updated"}


@pytest.mark.integration
async def test_change_password_wrong_without_user__fail(
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
    "new_password",
    [
        ("12345qwerty"),
        ("azertyuiop"),
        ("5555555555"),
        ("sweetheart"),
        ("PolniyPizdec0211"),
        ("пїЅпїЅпїЅпїЅпїЅпїЅ"),
        ("user123"),
    ],
)
@pytest.mark.integration
async def test_login__fail(
    new_password: str,
    get_user: UserSignUpIn,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.put(
        "/api/v1/users/change_password",
        json={
            "email": get_user.email,
            "old_password": get_user.password,
            "new_password": new_password,
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
