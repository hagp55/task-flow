import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.apps.projects.schemas import ProjectOut
from src.apps.tasks.schemas import TaskIn


@pytest.mark.integration
async def test_get_project_tasks__success(
    get_project_tasks: list[TaskIn],
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
            "projectId": str(task.project_id),
            "priority": task.priority,
            "status": task.status,
        }
        for task in get_project_tasks[::-1]
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
async def test_get_project_task__success(
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
    assert response.json()["projectId"] == get_task["projectId"]
    assert response.json()["priority"] == get_task["priority"]
    assert response.json()["status"] == get_task["status"]
    assert ProjectOut.model_validate(response.json())
