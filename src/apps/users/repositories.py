import logging
from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.orm import sessionmaker

from src.apps.users.models import User

logger = logging.getLogger(__name__)


@dataclass
class UsersRepository:
    db_session: sessionmaker

    async def create(
        self,
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        google_access_token: str | None = None,
        yandex_access_token: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User | None:
        statement = (
            insert(User)
            .values(
                username=username,
                password=password,
                email=email,
                google_access_token=google_access_token,
                yandex_access_token=yandex_access_token,
                first_name=first_name,
                last_name=last_name,
            )
            .returning(User.id)
        )
        logger.debug(statement)
        with self.db_session() as session:
            user_id: int = session.execute(statement).scalar()
            session.commit()
            return self.get(user_id)

    def get(self, user_id) -> User | None:
        statement = select(User).where(User.id == user_id)
        logger.debug(statement)
        with self.db_session() as session:
            return session.execute(statement).scalar_one_or_none()

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        logger.debug(statement)
        with self.db_session() as session:
            return session.execute(statement).scalar_one_or_none()

    def get_user_by_email(self, email) -> User | None:
        statement = select(User).where(User.email == email)
        logger.debug(statement)
        with self.db_session() as session:
            return session.execute(statement).scalar_one_or_none()
