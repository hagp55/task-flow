import logging
from pathlib import Path
from typing import Any

import jinja2
from fastapi import APIRouter, FastAPI, Request
from fastapi.datastructures import FormData
from jinja2 import FileSystemLoader
from jose import JWTError
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend

from src.apps.auth.services import AuthService
from src.apps.projects.admin import ProjectAdmin
from src.apps.tasks.admin import TaskAdmin
from src.apps.users.admin import UserAdmin
from src.apps.users.models import User
from src.apps.users.repositories import UsersRepository
from src.core.db import AsyncSessionFactory, engine
from src.core.settings import settings
from src.dependencies import get_users_repository
from src.exceptions import TokenExpiredException, TokenHasNotValidSignatureException, UserNotCorrectPasswordException

logger = logging.getLogger(__name__)
router = APIRouter()


def init_admin(_app: FastAPI) -> None:
    admin = Admin(
        _app,
        engine,
        title=settings.ADMIN_TITLE,
        base_url=f"/{settings.ADMIN_URL}",
        authentication_backend=authentication_backend,
    )
    loader: jinja2.BaseLoader | None = admin.templates.env.loader
    custom_templates = str(Path(__file__).parents[2] / "templates")
    if isinstance(loader, FileSystemLoader):
        loader.searchpath.insert(0, custom_templates)
    elif isinstance(loader, jinja2.ChoiceLoader):
        for sub_loader in loader.loaders:
            if isinstance(sub_loader, FileSystemLoader):
                sub_loader.searchpath.insert(0, custom_templates)
                break
    admin.add_view(UserAdmin)
    admin.add_view(ProjectAdmin)
    admin.add_view(TaskAdmin)


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form: FormData = await request.form()
        email = str(form["email"])
        password = str(form["password"])

        async with AsyncSessionFactory() as session:
            try:
                user_repository: UsersRepository = get_users_repository(session=session)
                user: User | None = await user_repository.get_user_by_email(email=email)
                if user is None or not user.is_active or not (user.is_staff or user.is_super_user):
                    return False
                AuthService._validate_auth_user(user=user, password=password)
            except UserNotCorrectPasswordException:
                return False
        token: str = AuthService.generate_access_token(user_id=user.id)
        request.session.update({"token": token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token: Any | None = request.session.get("token")
        if token:
            try:
                if AuthService.get_user_id_from_access_token(access_token=token):
                    return True
            except (TokenExpiredException, TokenHasNotValidSignatureException, JWTError):
                return False
        return False


authentication_backend = AdminAuth(secret_key=settings.JWT_SECRET_KEY)
