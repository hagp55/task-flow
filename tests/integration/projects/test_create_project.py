import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.apps.projects.schemas import ProjectOut


@pytest.mark.integration
async def test_create_project__success(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json={"name": "TaskMania"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert ProjectOut.model_validate(response.json())


@pytest.mark.integration
async def test_create_exists_project__fail(
    get_access_token: str,
    get_project: dict,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json={"name": get_project["name"]},
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "Project already exists"}


@pytest.mark.integration
async def test_create_project_not_authorized__fail(
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.post(
        "/api/v1/projects",
        json={"name": "TaskMania"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize(
    "name",
    [
        (""),
        ("" * 10),
        ("a"),
        ("a" * 251),
        (None),
    ],
)
@pytest.mark.integration
async def test_create_project_no_valid_payload__fail(
    name: str,
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json={"name": name},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.integration
async def test_create_project_without_payload__fail(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
