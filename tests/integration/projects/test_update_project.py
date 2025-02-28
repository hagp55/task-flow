import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.apps.projects.schemas import ProjectOut


@pytest.mark.integration
async def test_update_project__success(
    get_access_token: str,
    get_project: dict,
    async_client: AsyncClient,
) -> None:
    new_payload: dict[str, str] = {"name": f"{get_project['name']} v1.0"}
    response: Response = await async_client.put(
        f"/api/v1/projects/{get_project['id']}",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json=new_payload,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == new_payload["name"]
    assert ProjectOut.model_validate(response.json())


@pytest.mark.integration
async def test_update_not_exists_project__fail(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.put(
        "/api/v1/projects/1",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json={"name": "TaskMania"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Project not found"}


@pytest.mark.integration
async def test_update_project_not_authorized__fail(
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.put(
        "/api/v1/projects/1",
        json={"name": "TaskMania"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize(
    "name",
    [
        (""),
        (" " * 10),
        ("a"),
        ("a" * 251),
        (None),
    ],
)
@pytest.mark.integration
async def test_update_project_no_valid_payload__success(
    name: str,
    get_project: dict,
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.put(
        f"/api/v1/projects/{get_project['id']}",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json={"name": name},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
