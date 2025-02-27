import pytest
from httpx import AsyncClient, Response
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.auth.security import bcrypt_context
from src.apps.users.models import User
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


@pytest.fixture
async def get_user_staff(
    session: AsyncSession,
) -> UserSignUpIn:
    user = UserSignUpIn(
        email="user@example.com",
        password="strong_password",
    )
    hashed_password: str = bcrypt_context.hash(user.password)
    updated_payload = user.model_copy(update={"password": hashed_password})
    await session.execute(
        insert(
            User,
        ).values(is_staff=True, **updated_payload.model_dump())
    )
    await session.commit()
    return user


@pytest.fixture
async def get_user_superuser(
    session: AsyncSession,
) -> UserSignUpIn:
    user = UserSignUpIn(
        email="user@example.com",
        password="strong_password",
    )
    hashed_password: str = bcrypt_context.hash(user.password)
    updated_payload = user.model_copy(update={"password": hashed_password})
    await session.execute(
        insert(
            User,
        ).values(is_super_user=True, **updated_payload.model_dump())
    )
    await session.commit()
    return user


@pytest.fixture
async def get_access_token(async_client: AsyncClient) -> str:
    user = UserSignUpIn(
        email="user@example.com",
        password="strong_password",
    )
    response: Response = await async_client.post(
        "/api/v1/users/signup",
        json=user.model_dump(),
    )
    return response.json().get("accessToken", "")


@pytest.fixture
async def get_access_token_staff(
    get_user_staff: UserSignUpIn,
    async_client: AsyncClient,
) -> str:
    response: Response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": get_user_staff.email,
            "password": get_user_staff.password,
        },
    )
    return response.json().get("accessToken", "")


@pytest.fixture
async def get_access_token_superuser(
    get_user_superuser: UserSignUpIn,
    async_client: AsyncClient,
) -> str:
    response: Response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": get_user_superuser.email,
            "password": get_user_superuser.password,
        },
    )
    return response.json().get("accessToken", "")
