import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.apps.tasks.schemas import TaskOut


@pytest.mark.integration
async def test_update_task__success(
    get_access_token: str,
    get_project_task: dict,
    async_client: AsyncClient,
) -> None:
    new_payload: dict[str, str] = {
        "name": f"{get_project_task['name']} v1.0",
        "project_id": get_project_task["id"],
        "priority": "medium",
        "status": "completed",
    }
    response: Response = await async_client.put(
        f"/api/v1/tasks/{get_project_task['id']}",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json=new_payload,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == new_payload["name"]
    assert response.json()["priority"] == new_payload["priority"]
    assert response.json()["status"] == new_payload["status"]
    assert TaskOut.model_validate(response.json())


@pytest.mark.integration
async def test_update_not_task_not_exists_project__fail(
    get_access_token: str,
    get_task: dict,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.put(
        "/api/v1/tasks/1",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json={
            "name": "TaskMania",
            "project_id": 1,
            "priority": "medium",
            "status": "completed",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Project not found"}
