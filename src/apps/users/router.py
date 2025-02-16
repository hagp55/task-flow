from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.apps.users.schemas import UserIn, UserLoginOut
from src.apps.users.services import UsersService
from src.dependencies import get_users_service

__all__ = ("router",)


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserLoginOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserIn,
    users_service: Annotated[UsersService, Depends(get_users_service)],
) -> UserLoginOut:
    return await users_service.create(
        payload.username,
        payload.password,
    )
