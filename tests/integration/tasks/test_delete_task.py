import pytest
from fastapi import status
from httpx import AsyncClient, Response


@pytest.mark.integration
async def test_delete_task__success(
    get_access_token: str,
    get_task: dict,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.delete(
        "/api/v1/tasks/1",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.integration
async def test_delete_not_exists_task__success(
    get_access_token: str,
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.delete(
        "/api/v1/tasks/1",
        headers={"Authorization": f"Bearer {get_access_token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Task not found"}


@pytest.mark.integration
async def test_delete_projects_not_authorized__success(
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.delete(
        "/api/v1/tasks/1",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Not authenticated"}
