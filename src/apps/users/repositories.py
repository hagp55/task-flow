import logging
from dataclasses import dataclass

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.users.models import User
from src.core.db import engine
from src.core.utils.time import now

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

    async def get_user_by_email(self, *, email) -> User | None:
        query = select(User).where(User.email == email)
        logger.debug("Query:\n%s" % (query.compile(engine, compile_kwargs={"literal_binds": True})))
        return (await self.db_session.execute(query)).scalar()

    async def update_last_login(self, *, user_id) -> None:
        await self.db_session.execute(
            update(User)
            .where(
                User.id == user_id,
            )
            .values(last_login=now())
        )
        await self.db_session.commit()
