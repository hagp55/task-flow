import uuid
from typing import Any

import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.apps.tasks.schemas import TaskOut


@pytest.mark.parametrize(
    "name,priority,task_status",
    [
        ("Spend 10 minutes meditating to clear the mind.", "low", "pending"),
        ("Spend 10 minutes meditating to clear the mind.", "medium", "pending"),
        ("Spend 10 minutes meditating to clear the mind.", "high", "pending"),
        ("Spend 10 minutes meditating to clear the mind.", "low", "pending"),
        ("Spend 10 minutes meditating to clear the mind.", "low", "progress"),
        ("Spend 10 minutes meditating to clear the mind.", "low", "completed"),
    ],
)
@pytest.mark.integration
async def test_create_project_task__success(
    name: str,
    priority: str,
    task_status: str,
    get_project,
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    payload: dict[str, Any] = {
        "name": name,
        "priority": priority,
        "project_id": get_project["id"],
        "status": task_status,
    }
    response: Response = await async_client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json=payload,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["projectId"] == get_project["id"]
    assert TaskOut.model_validate(response.json())


@pytest.mark.integration
async def test_create_project_task_not_exists_project__fail(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    data: dict[str, str | None | uuid.UUID] = {
        "name": "Spend 10 minutes meditating to clear the mind.",
        "projectId": str(uuid.uuid4()),
        "priority": "low",
        "status": "pending",
    }
    response: Response = await async_client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Project not found"}
