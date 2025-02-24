from dataclasses import dataclass

from src.apps.auth.security import bcrypt_context
from src.apps.auth.services import AuthService
from src.apps.users.models import User
from src.apps.users.repositories import UsersRepository
from src.apps.users.schemas import UserLoginOut, UserMeOut, UserSignUpIn
from src.exceptions import UserAlreadyExistsException, UserNotFoundException


@dataclass
class UsersService:
    users_repository: UsersRepository
    auth_service: AuthService

    async def create(self, *, payload: UserSignUpIn) -> UserLoginOut:
        exists_user: User | None = await self.users_repository.get_user_by_email(email=payload.email)
        if exists_user:
            raise UserAlreadyExistsException
        hashed_password: str = bcrypt_context.hash(payload.password)
        updated_payload: UserSignUpIn = payload.model_copy(update={"password": hashed_password})
        user: User | None = await self.users_repository.create(**updated_payload.model_dump())
        access_token: str = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginOut(id=user.id, access_token=access_token)

    async def get(self, *, user_id: int) -> UserMeOut:
        user: User | None = await self.users_repository.get(user_id=user_id)
        if not user:
            raise UserNotFoundException
        return UserMeOut.model_validate(user)
