from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.apps.users.schemas import ChangeUserPasswordIn, UserLoginOut, UserMeOut, UserSignUpIn
from src.apps.users.services import UsersService
from src.dependencies import get_request_user_id, get_users_service
from src.exceptions import UserAlreadyExistsException, UserNotCorrectPasswordException, UserNotFoundException

__all__ = ("router",)


router = APIRouter()


@router.post(
    "/signup",
    response_model=UserLoginOut,
    summary="Registering a new user 🙌",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    payload: UserSignUpIn,
    users_service: Annotated[UsersService, Depends(get_users_service)],
) -> UserLoginOut:
    """
    Register a new user with the provided information.

    - **email**: The email address of the user (must be between 6 and 250 characters).
    - **password**: The password for the user account (must be between 6 and 250 characters).
    - **first_name**: Optional first name of the user (if provided, should be between 2 and 250 characters).
    - **last_name**: Optional last name of the user (if provided, should be between 2 and 255 characters).

    **Response**:
    - `201 Created`: Returns the newly created user's ID and an access token for authentication.

    **Errors**:
    - `409 Conflict`: If the user with the provided email already exists.
    """
    try:
        return await users_service.create(payload=payload)
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e.detail),
        )


@router.put(
    "/change_password",
    name="Change password by user ✏️",
    status_code=status.HTTP_200_OK,
)
async def user_change_password(
    payload: ChangeUserPasswordIn,
    users_service: Annotated[UsersService, Depends(get_users_service)],
) -> dict[str, str]:
    """
    Change the password for a user.

    - **email**: The email address of the user whose password is being updated.
    - **old_password**: The current password of the user.
    - **new_password**: The new password that the user wants to set.

    **Response**:
    - `200 OK`: A success message confirming that the password has been updated.

    **Errors**:
    - `400 Bad Request`: If the user is not found or the old password provided is incorrect.
    """
    try:
        await users_service.change_password(payload=payload)
        return {"message": "password was successfully updated"}
    except (UserNotFoundException, UserNotCorrectPasswordException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.detail),
        )


@router.get(
    "/me",
    response_model=UserMeOut,
    name="Get info about me 🧐",
    status_code=status.HTTP_200_OK,
)
async def me(
    users_service: Annotated[UsersService, Depends(get_users_service)],
    user_id: int = Depends(get_request_user_id),
) -> UserMeOut:
    """
    Get information about the authenticated user.

    **Response**:
    - Returns details about the authenticated user, including:
      - **first_name**: The user's first name.
      - **last_name**: The user's last name.
      - **email**: The user's email address.
      - **is_active**: The status indicating if the user is active.
      - **is_staff**: The status indicating if the user is a staff member.
      - **is_super_user**: The status indicating if the user is a superuser.
      - **date_joined**: The timestamp when the user account was created.
      - **last_login**: The timestamp of the user's last login.

    **Errors**:
    - `401 Unauthorized`: If the user is not authenticated or not found.
    """
    try:
        return await users_service.get(user_id=user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e.detail),
        )
