from dataclasses import dataclass

from src.apps.users.models import User
from src.apps.users.repositories import UsersRepository
from src.apps.users.schemas import UserLoginOut
from src.exceptions import UserNotCorrectPasswordException, UserNotFoundException


@dataclass
class AuthService:
    users_repository: UsersRepository

    def login(self, username: str, password: str) -> UserLoginOut:
        user: User | None = self.users_repository.get_by_username(
            username=username,
        )
        self._validate_auth_user(user, password)
        return UserLoginOut.model_validate(user)

    @staticmethod
    def _validate_auth_user(user: User, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException
