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
async def test_create_task__success(
    name: str,
    priority: str,
    task_status: str,
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    payload: dict[str, Any] = {
        "name": name,
        "priority": priority,
        "status": task_status,
    }
    response: Response = await async_client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json=payload,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert TaskOut.model_validate(response.json())


@pytest.mark.integration
async def test_create_task_default_status__success(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    payload: dict[str, Any] = {
        "name": "Spend 10 minutes meditating to clear the mind.",
        "projectId": None,
        "priority": "low",
    }
    response: Response = await async_client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json=payload,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert TaskOut.model_validate(response.json())


@pytest.mark.integration
async def test_create_task_default_priority__success(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    payload: dict[str, Any] = {
        "name": "Spend 10 minutes meditating to clear the mind.",
        "projectId": None,
        "status": "pending",
    }
    response: Response = await async_client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json=payload,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert TaskOut.model_validate(response.json())


@pytest.mark.integration
async def test_create_exists_task__fail(
    get_task: dict,
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    data: dict[str, str | None] = {
        "name": "Spend 10 minutes meditating to clear the mind.",
        "projectId": None,
        "priority": "low",
        "status": "pending",
    }
    response: Response = await async_client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json=data,
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "Task already exists"}


@pytest.mark.integration
async def test_create_task_not_authorized__fail(
    async_client: AsyncClient,
) -> None:
    data: dict[str, str | None] = {
        "name": "Spend 10 minutes meditating to clear the mind.",
        "projectId": None,
        "priority": "low",
        "status": "pending",
    }
    response: Response = await async_client.post(
        "/api/v1/tasks",
        json=data,
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
async def test_create_task_no_valid_payload__fail(
    name: str,
    priority: str,
    task_status: str,
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    payload: dict[str, Any] = {
        "name": name,
        "priority": priority,
        "status": task_status,
    }
    response: Response = await async_client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json={"name": payload},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
