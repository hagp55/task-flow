import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.apps.users.schemas import UserLoginOut


@pytest.mark.parametrize(
    "email,password,first_name,last_name",
    [
        ("valid@domain.com", "strongPassword12d!", None, None),
        ("valid@domain.com", "strongPassword12d", "John", None),
        ("valid@domain.com", "strongPassword12d", "John", "Doe"),
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
        ("valid@domain.com", "strongPassword12d"),
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


@pytest.mark.parametrize(
    "email,password,first_name,last_name",
    [
        ("valid@domain.com", "1323455463445243", None, None),
        ("valid@domain.com", "valid45", None, None),
        ("valid@domain.com", "111222tianya", None, None),
        ("valid@domain.com", "421uiopy258", None, None),
        ("valid@domain.com", "password123", "valid", None),
        ("valid@domain.com", "PE#5GZ29PTZMSE", None, "valid"),
        ("valid@domain.com", "1323455463445243", None, "valid"),
        ("valid@domain.com", "valid45", None, None),
        ("valid@domain.com", "computer1", None, "valid"),
        ("valid@domain.com", "qwerty12345", None, "valid"),
    ],
)
@pytest.mark.integration
async def test_create_user_no_valid_password__fail(
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
