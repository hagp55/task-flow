import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from src.apps.auth.services import AuthService
from src.apps.users.schemas import UserIn, UserLoginOut
from src.dependencies import get_auth_service
from src.exceptions import UserNotCorrectPasswordException, UserNotFoundException

router = APIRouter(prefix="/auth", tags=["Auth"])
logging = logging.getLogger(__name__)


@router.post("/login", response_model=UserLoginOut, status_code=status.HTTP_200_OK)
def login_user(
    payload: UserIn,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserLoginOut:
    try:
        return auth_service.login(
            payload.username,
            payload.password,
        )
    except (
        UserNotFoundException,
        UserNotCorrectPasswordException,
    ) as e:
        raise HTTPException(status_code=401, detail=e.detail)


@router.get("/login/google", response_class=RedirectResponse)
def login_user_with_google(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RedirectResponse:
    redirect_url: str = auth_service.get_google_redirect_url()
    logging.debug(redirect_url)
    return RedirectResponse(url=redirect_url)


@router.get("/google")
def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str,
):
    return auth_service.google_auth(code=code)
