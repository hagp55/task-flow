import logging
from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.orm import sessionmaker

from src.apps.users.models import User

logger = logging.getLogger(__name__)


@dataclass
class UsersRepository:
    db_session: sessionmaker

    def create(self, username: str, password: str) -> User | None:
        statement = (
            insert(User)
            .values(
                username=username,
                password=password,
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
