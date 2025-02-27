import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.apps.users.schemas import UserMeOut, UserSignUpIn


@pytest.mark.integration
async def test_user_me__success(
    get_user: UserSignUpIn,
    async_client: AsyncClient,
) -> None:
    login_user: Response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": get_user.email,
            "password": get_user.password,
        },
    )
    access_token: str = login_user.json().get("accessToken")
    response: Response = await async_client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert UserMeOut.model_validate(response.json())


@pytest.mark.parametrize(
    "access_token",
    [
        ("ss",),
        (None,),
        ("",),
        ("abc" * 200),
    ],
)
@pytest.mark.integration
async def test_user_me__fail(
    access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Token has not valid signature"}


@pytest.mark.integration
async def test_user_me_without_headers__fail(
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/users/me",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}
