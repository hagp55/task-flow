import uuid

import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.apps.projects.schemas import ProjectIn, ProjectOut


@pytest.mark.integration
async def test_get_empty_projects__success(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.integration
async def test_get_projects__success(
    get_access_token: str,
    get_projects: list[ProjectIn],
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )
    input_names: set[str] = {project.name for project in get_projects}
    response_names: set[str] = {project["name"] for project in response.json()}

    assert response.status_code == status.HTTP_200_OK
    assert input_names == response_names


@pytest.mark.integration
async def test_get_project__success(
    get_access_token: str,
    get_project: dict,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        f"/api/v1/projects/{get_project['id']}",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == get_project["name"]
    assert ProjectOut.model_validate(response.json())


@pytest.mark.integration
async def test_get_not_exists_project__fail(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        f"/api/v1/projects/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Project not found"}


@pytest.mark.integration
async def test_get_projects_not_authorized__fail(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/projects",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}
