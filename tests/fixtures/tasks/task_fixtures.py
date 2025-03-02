import pytest
from httpx import AsyncClient, Response

from src.apps.tasks.enums import Priority, Status
from src.apps.tasks.schemas import TaskIn


@pytest.fixture
async def get_task(
    get_access_token: str,
    async_client: AsyncClient,
) -> dict:
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
    return response.json()


@pytest.fixture
async def get_project_task(
    get_project: dict,
    get_access_token: str,
    async_client: AsyncClient,
) -> dict:
    data: dict[str, str | None] = {
        "name": "Spend 10 minutes meditating to clear the mind.",
        "projectId": get_project["id"],
        "priority": "low",
        "status": "pending",
    }
    response: Response = await async_client.post(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json=data,
    )
    return response.json()


@pytest.fixture
async def get_tasks(
    get_access_token: str,
    async_client: AsyncClient,
) -> list[TaskIn]:
    tasks: list[TaskIn] = [
        TaskIn(name="Meditaion", priority=Priority.high, status=Status.pending),
        TaskIn(name="Meditaion1", priority=Priority.high, status=Status.pending),
        TaskIn(name="Meditaion2", priority=Priority.high, status=Status.pending),
        TaskIn(name="Meditaion3", priority=Priority.high, status=Status.pending),
    ]
    for task in tasks:
        response: Response = await async_client.post(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {get_access_token}"},
            json=task.model_dump(),
        )
    return tasks


@pytest.fixture
async def get_project_tasks(
    get_project: dict,
    get_access_token: str,
    async_client: AsyncClient,
) -> list[TaskIn]:
    tasks: list[TaskIn] = [
        TaskIn(name="Meditaion", priority=Priority.high, status=Status.pending, project_id=get_project["id"]),
        TaskIn(name="Meditaion1", priority=Priority.high, status=Status.pending, project_id=get_project["id"]),
        TaskIn(name="Meditaion2", priority=Priority.high, status=Status.pending, project_id=get_project["id"]),
        TaskIn(name="Meditaion3", priority=Priority.high, status=Status.pending, project_id=get_project["id"]),
    ]
    for task in tasks:
        response: Response = await async_client.post(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {get_access_token}"},
            json=task.model_dump(mode="json"),
        )
    return tasks
