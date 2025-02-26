import pytest
from httpx import AsyncClient, Response

from src.apps.users.schemas import UserSignUpIn


@pytest.fixture
async def get_user(async_client: AsyncClient) -> UserSignUpIn:
    user = UserSignUpIn(
        email="user@example.com",
        password="strong_password",
        first_name="first_name",
        last_name="last_name",
    )
    response: Response = await async_client.post(
        "/api/v1/users/signup",
        json=user.model_dump(),
    )
    return user
