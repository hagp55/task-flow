import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.apps.users.schemas import UserLoginOut


@pytest.mark.parametrize(
    "email,password,first_name,last_name",
    [
        ("valid@domain.com", "password", None, None),
        ("valid@domain.com", "password", "John", None),
        ("valid@domain.com", "password", "John", "Doe"),
    ],
)
@pytest.mark.integration
async def test_create_user__success(
    email: str,
    password: str,
    first_name: str | None,
    last_name: str | None,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.post(
        "/api/v1/users/signup",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert UserLoginOut.model_validate(response.json())


@pytest.mark.parametrize(
    "email,password",
    [
        ("valid@domain.com", "password"),
    ],
)
@pytest.mark.integration
async def test_create_user_only_required_fields__success(
    email: str,
    password: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.post(
        "/api/v1/users/signup",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert UserLoginOut.model_validate(response.json())


@pytest.mark.integration
async def test_create_exists_user__fail(async_client: AsyncClient) -> None:
    response: Response = await async_client.post(
        "/api/v1/users/signup",
        json={
            "email": "beazley@example.com",
            "password": "Str0ngP@ssw0rd!",
            "first_name": "test_user",
            "last_name": "test_user",
        },
    )

    response = await async_client.post(
        "/api/v1/users/signup",
        json={
            "email": "beazley@example.com",
            "password": "Str0ngP@ssw0rd!",
            "first_name": "test_user",
            "last_name": "test_user",
        },
    )
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "email,password,first_name,last_name",
    [
        ("novaliddomain.ru", "password", None, None),
        (None, "password", None, None),
        ("v@d.c", "password", "John", "Doe"),
        ("valid@domain.com", "pass", "John", "Doe"),
        ("valid@domain.com", "pass" * 100, "John", "Doe"),
        ("valid@domain.com", None, "John", "Doe"),
        ("valid@domain.com", " " * 10, "John", "Doe"),
        ("valid@domain.com", "password", " " * 10, ""),
        ("valid@domain.com", "password", "a", ""),
        ("valid@domain.com", "password", "a" * 251, "Doe"),
        ("valid@domain.com", "password", "John", " " * 10),
        ("valid@domain.com", "password", "John", "a"),
        ("valid@domain.com", "password", "", " " * 251),
    ],
)
@pytest.mark.integration
async def test_create_user_no_valid_payload__fail(
    email: str,
    password: str,
    first_name: str | None,
    last_name: str | None,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.post(
        "/api/v1/users/signup",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
