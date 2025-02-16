from dataclasses import dataclass

from src.apps.auth.services import AuthService
from src.apps.users.models import User
from src.apps.users.repositories import UsersRepository
from src.apps.users.schemas import UserLoginOut


@dataclass
class UsersService:
    users_repository: UsersRepository
    auth_service: AuthService

    def create(self, username: str, password: str) -> UserLoginOut:
        user: User | None = self.users_repository.create(
            username=username,
            password=password,
        )
        access_token: str = self.auth_service.generate_access_token(user.id)
        return UserLoginOut(
            id=user.id,
            access_token=access_token,
        )
