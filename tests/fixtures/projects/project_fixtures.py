import pytest
from httpx import AsyncClient, Response

from src.apps.projects.schemas import ProjectIn


@pytest.fixture
async def get_project(
    get_access_token: str,
    async_client: AsyncClient,
) -> dict:
    data: dict[str, str] = {"name": "TaskMania"}
    response: Response = await async_client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {get_access_token}"},
        json=data,
    )
    return response.json()


@pytest.fixture
async def get_projects(
    get_access_token: str,
    async_client: AsyncClient,
) -> list[ProjectIn]:
    projects: list[ProjectIn] = [
        ProjectIn(name="TaskMania1"),
        ProjectIn(name="TaskMania2"),
        ProjectIn(name="TaskMania3"),
        ProjectIn(name="TaskMania4"),
        ProjectIn(name="TaskMania5"),
    ]
    for project in projects:
        response: Response = await async_client.post(
            "/api/v1/projects",
            headers={"Authorization": f"Bearer {get_access_token}"},
            json=project.model_dump(),
        )
    return projects
