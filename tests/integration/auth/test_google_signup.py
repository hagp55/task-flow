import pytest
from fastapi import status
from httpx import AsyncClient, Response

from src.core.settings import settings


@pytest.mark.integration
async def test_redirect_status_code_google_signup__success(
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get("/api/v1/auth/login/google")
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT


@pytest.mark.integration
async def test_redirect_google_signup__success(
    async_client: AsyncClient,
) -> None:
    response: Response = await async_client.get(
        "/api/v1/auth/login/google",
        follow_redirects=True,
    )
    assert response.url == settings.GOOGLE_REDIRECT_URL
