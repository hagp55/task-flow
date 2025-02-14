import string
from dataclasses import dataclass
from random import choice

from src.apps.users.models import User
from src.apps.users.repositories import UsersRepository
from src.apps.users.schemas import UserLoginOut


@dataclass
class UsersService:
    users_repository: UsersRepository

    def create(self, username: str, password: str) -> UserLoginOut:
        access_token = self._generate_access_token()
        user: User | None = self.users_repository.create(
            username=username,
            password=password,
            access_token=access_token,
        )
        return UserLoginOut(
            user_id=user.id,
            access_token=user.access_token,
        )

    @staticmethod
    def _generate_access_token() -> str:
        return "".join(choice(string.ascii_uppercase + string.digits) for _ in range(10))
