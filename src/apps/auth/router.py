from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.apps.auth.services import AuthService
from src.apps.users.schemas import UserIn, UserLoginOut
from src.dependencies import get_auth_service
from src.exceptions import UserNotCorrectPasswordException, UserNotFoundException

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=UserLoginOut, status_code=status.HTTP_201_CREATED)
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
