import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from src.apps.auth.services import AuthService
from src.apps.users.schemas import UserLoginIn, UserLoginOut
from src.dependencies import get_auth_service
from src.exceptions import UserNotCorrectPasswordException, UserNotFoundException

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/login",
    response_model=UserLoginOut,
    name="User login 🤝",
    status_code=status.HTTP_200_OK,
)
async def login_user(
    payload: UserLoginIn,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserLoginOut:
    try:
        return await auth_service.login(payload.email, payload.password)
    except (
        UserNotFoundException,
        UserNotCorrectPasswordException,
    ) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e.detail),
        )


@router.get(
    "/login/google",
    response_class=RedirectResponse,
    name="For signup 🤗 Go to link in description ✨🚀",
    description="Go to the link in any browser <b>http://localhost:8000/api/v1/auth/login/google</b>",
)
async def login_user_with_google(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RedirectResponse:
    redirect_url: str = auth_service.get_google_redirect_url()
    return RedirectResponse(url=redirect_url)


@router.get(
    "/google",
    name="Google authorization 🤗",
)
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str,
) -> UserLoginOut:
    return await auth_service.google_auth(code=code)


@router.get(
    "/login/yandex",
    response_class=RedirectResponse,
    name="For signup 🤗 Go to link in description ✨🚀",
    description="Go to the link in any browser <b>http://localhost:8000/api/v1/auth/login/yandex</b>",
)
async def login_user_with_yandex(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RedirectResponse:
    redirect_url: str = auth_service.get_yandex_redirect_url()
    return RedirectResponse(url=redirect_url)


@router.get(
    "/yandex",
    name="Yandex authorization 🤗",
)
async def yandex_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str,
) -> UserLoginOut:
    return await auth_service.yandex_auth(code=code)
