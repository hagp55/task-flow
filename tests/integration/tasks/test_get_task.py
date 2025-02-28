import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.apps.projects.schemas import ProjectOut
from src.apps.tasks.schemas import TaskIn


@pytest.mark.integration
async def test_get_empty_tasks__success(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.integration
async def test_get_tasks__success(
    get_tasks: list[TaskIn],
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )
    input_data = [
        {
            "name": task.name,
            "projectId": task.project_id,
            "priority": task.priority,
            "status": task.status,
        }
        for task in get_tasks[::-1]
    ]
    output_data = [
        {
            "name": task["name"],
            "projectId": task["projectId"],
            "priority": task["priority"],
            "status": task["status"],
        }
        for task in response.json()
    ]

    assert response.status_code == status.HTTP_200_OK
    assert input_data == output_data


@pytest.mark.integration
async def test_get_task__success(
    get_access_token: str,
    get_task: dict,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        f"/api/v1/tasks/{get_task['id']}",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == get_task["name"]
    assert ProjectOut.model_validate(response.json())


@pytest.mark.integration
async def test_get_not_exists_task__fail(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/tasks/1",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Task not found"}


@pytest.mark.integration
async def test_get_projects_not_authorized__fail(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/tasks",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}
