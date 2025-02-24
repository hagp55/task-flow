from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.apps.users.schemas import UserLoginOut, UserMeOut, UserSignUpIn
from src.apps.users.services import UsersService
from src.core.dependencies import get_request_user_id, get_users_service
from src.exceptions import UserAlreadyExistsException, UserNotFoundException

__all__ = ("router",)


router = APIRouter()


@router.post(
    "/",
    response_model=UserLoginOut,
    summary="Registering a new user 🙌",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    payload: UserSignUpIn,
    users_service: Annotated[UsersService, Depends(get_users_service)],
) -> UserLoginOut:
    try:
        return await users_service.create(payload=payload)
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.detail),
        )


@router.get(
    "/me",
    response_model=UserMeOut,
    summary="Get info about me 🧐",
    status_code=status.HTTP_200_OK,
)
async def me(
    users_service: Annotated[UsersService, Depends(get_users_service)],
    user_id: int = Depends(get_request_user_id),
) -> UserMeOut:
    try:
        return await users_service.get(user_id=user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e.detail),
        )
