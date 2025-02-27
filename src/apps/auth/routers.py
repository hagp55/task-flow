import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from src.apps.auth.services import AuthService
from src.apps.users.schemas import UserLoginIn, UserLoginOut
from src.dependencies import get_auth_service
from src.exceptions import UserNotCorrectPasswordException

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
    """
    Authenticate a user and get a login token.

    **Request**:
    - **email**: The user's email address.
    - **password**: The user's password.

    **Response**:
    - Returns an access token along with the user's ID if the credentials are valid.

    **Errors**:
    - `401 Unauthorized`: If the credentials are incorrect (invalid email or password).
    """
    try:
        return await auth_service.login(payload.email, payload.password)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e.detail),
        )


@router.get(
    "/login/google",
    response_class=RedirectResponse,
    name="For signup 🤗 Go to link in description ✨🚀",
    # description="Go to the link in any browser <b>http://localhost:8000/api/v1/auth/login/google</b>",
)
async def login_user_with_google(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RedirectResponse:
    """
    Redirect the user to the Google authentication page for login or signup.
    Go in browser <b>http://localhost:8000/api/v1/auth/login/google</b>
    This endpoint generates a Google authentication URL and redirects the user to it.
    The user can log in or sign up using their Google account.

    **Response**:
    - Redirects the user to the Google authentication page.
    """
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
    """
    Handle the callback from Google authentication.

    After the user has successfully logged in via Google, this endpoint processes the authorization code
    provided by Google and exchanges it for an access token.

    **Parameters**:
    - `code`: The authorization code returned by Google after user login.

    **Response**:
    - Returns a `UserLoginOut` object containing the user's ID and access token.
    """
    return await auth_service.google_auth(code=code)


@router.get(
    "/login/yandex",
    response_class=RedirectResponse,
    name="For signup 🤗 Go to link in description ✨🚀",
    # description="Go to the link in any browser <b>http://localhost:8000/api/v1/auth/login/yandex</b>",
)
async def login_user_with_yandex(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RedirectResponse:
    """
    Redirect the user to Yandex authorization page for login/signup.
    Go in browser <b>http://localhost:8000/api/v1/auth/login/yandex</b>
    This endpoint generates and returns a URL where the user can log in or sign up using their Yandex account.

    **Description**:
    - Go to the provided URL in a browser to start the Yandex authentication process.

    **Response**:
    - Redirects the user to the Yandex login/signup page.
    """
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
    """
    Handle the callback from Yandex authentication.

    After the user has successfully logged in via Yandex, this endpoint processes the authorization code
    provided by Yandex and exchanges it for an access token.

    **Parameters**:
    - `code`: The authorization code returned by Yandex after user login.

    **Response**:
    - Returns a `UserLoginOut` object containing the user's ID and access token.

    If the authentication process fails or the code is invalid, an error will be raised.
    """
    return await auth_service.yandex_auth(code=code)
