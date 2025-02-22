import logging
from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.users.models import User
from src.core.db import engine

logger = logging.getLogger(__name__)


@dataclass
class UsersRepository:
    db_session: AsyncSession

    async def create(self, **payload) -> User | None:
        query = (
            insert(User)
            .values(
                **payload,
            )
            .returning(User)
        )
        logger.debug("Query:\n%s" % (query.compile(engine, compile_kwargs={"literal_binds": True})))
        user: User | None = (await self.db_session.execute(query)).scalar()
        await self.db_session.commit()
        return user

    async def get(self, *, user_id) -> User | None:
        query = select(User).where(User.id == user_id)
        logger.debug("Query:\n%s" % (query.compile(engine, compile_kwargs={"literal_binds": True})))
        return (await self.db_session.execute(query)).scalar()

    async def get_user_by_username(self, *, username: str) -> User | None:
        query = select(User).where(User.username == username)
        logger.debug("Query:\n%s" % (query.compile(engine, compile_kwargs={"literal_binds": True})))
        return (await self.db_session.execute(query)).scalar()

    async def get_user_by_email(self, *, email) -> User | None:
        query = select(User).where(User.email == email)
        logger.debug("Query:\n%s" % (query.compile(engine, compile_kwargs={"literal_binds": True})))
        return (await self.db_session.execute(query)).scalar()
