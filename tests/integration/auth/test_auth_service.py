from collections.abc import Sequence

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.auth.services import AuthService
from src.apps.users.models import User
from src.apps.users.schemas import UserLoginOut


@pytest.mark.skip
async def test_google_auth__login_not_exists_user(
    auth_service: AuthService,
    db_session: AsyncSession,
) -> None:
    users: Sequence[User] = (await db_session.execute(select(User))).scalars().all()
    code = "fake_code"

    assert len(users) == 0
    user: UserLoginOut = await auth_service.google_auth(code)

    assert user is not None
    login_user = (await db_session.execute(select(User).where(User.id == user.id))).scalars().first()
    assert login_user is not None


# @pytest.mark.skip
# async def test_google_auth__login_exists_user(
#     auth_service: AuthService,
#     db_session: AsyncSession,
# ) -> None:
#     user = await db_session.execute(
#         insert(User).values(
#             id=EXISTS_GOOGLE_USER_ID,
#             email=EXISTS_GOOGLE_EMAIL,
#         )
#     )
#     await db_session.commit()
#     login_user: UserLoginOut = await auth_service.google_auth("fake_code")

#     assert user is not None
#     users: Sequence[User] = (await db_session.execute(select(User))).scalars().all()
#     assert len(users) == 1
#     assert login_user.id == EXISTS_GOOGLE_USER_ID


# async def test_base_login__success(
#     auth_service: AuthService,
#     db_session: AsyncSession,
# ) -> None:
#     password = "test_password"
#     user = await db_session.execute(
#         insert(User).values(
#             id=EXISTS_GOOGLE_USER_ID,
#             email=EXISTS_GOOGLE_EMAIL,
#             password=password,
#         )
#     )
#     await db_session.commit()
#     login_user: UserLoginOut = await auth_service.login(email, password)
#     assert bool(login_user) is True
