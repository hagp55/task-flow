import uuid
from typing import Any

import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.apps.tasks.schemas import TaskOut


@pytest.mark.integration
async def test_update_task__success(
    get_access_token: str,
    get_task: dict,
    async_client: AsyncClient,
) -> None:
    new_payload: dict[str, str] = {
        "name": f"{get_task['name']} v1.0",
        "priority": "medium",
        "status": "completed",
    }
    response: Response = await async_client.put(
        f"/api/v1/tasks/{get_task['id']}",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json=new_payload,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == new_payload["name"]
    assert response.json()["priority"] == new_payload["priority"]
    assert response.json()["status"] == new_payload["status"]
    assert TaskOut.model_validate(response.json())


@pytest.mark.integration
async def test_update_not_exists_task__fail(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.put(
        f"/api/v1/tasks/{uuid.uuid4()}",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json={
            "name": "TaskMania",
            "priority": "medium",
            "status": "completed",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Task not found"}


@pytest.mark.integration
async def test_update_task_not_authorized__fail(
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.put(
        f"/api/v1/tasks/{uuid.uuid4()}",
        json={
            "name": "TaskMania",
            "priority": "medium",
            "status": "completed",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.parametrize(
    "name,priority,task_status",
    [
        (" ", "low", "pending"),
        (" " * 10, "low", "pending"),
        (None, "low", "pending"),
        ("task", "pending!", "pending"),
        ("task", "low", "!pending!"),
    ],
)
@pytest.mark.integration
async def test_update_task_no_valid_payload__success(
    name: str,
    priority: str,
    task_status: str,
    get_project: dict,
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    payload: dict[str, Any] = {
        "name": name,
        "priority": priority,
        "status": task_status,
    }
    response: Response = await async_client.put(
        f"/api/v1/tasks/{get_project['id']}",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json=payload,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
