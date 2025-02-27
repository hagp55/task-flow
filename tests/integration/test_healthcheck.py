import pytest
from fastapi import status
from httpx import AsyncClient, Response


@pytest.mark.integration
async def test_healthcheck_api_staff__success(
    get_access_token_staff: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/healthcheck",
        headers={"Authorization": f"Bearer {get_access_token_staff}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "api is working."}


@pytest.mark.integration
async def test_healthcheck_api_superuser__success(
    get_access_token_superuser: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/healthcheck",
        headers={"Authorization": f"Bearer {get_access_token_superuser}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "api is working."}


@pytest.mark.integration
async def test_healthcheck_api_without_permissions__fail(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/healthcheck",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Permission denied"}


@pytest.mark.integration
async def test_healthcheck_api_unauthorized__fail(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/healthcheck",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.integration
async def test_healthcheck_db_staff__success(
    get_access_token_staff: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/healthcheck/db",
        headers={"Authorization": f"Bearer {get_access_token_staff}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "db is working."}


@pytest.mark.integration
async def test_healthcheck_db_superuser__success(
    get_access_token_superuser: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/healthcheck/db",
        headers={"Authorization": f"Bearer {get_access_token_superuser}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "db is working."}


@pytest.mark.integration
async def test_healthcheck_db_without_permissions__fail(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/healthcheck/db",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Permission denied"}


@pytest.mark.integration
async def test_healthcheck_db_unauthorized__fail(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/healthcheck/db",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}
