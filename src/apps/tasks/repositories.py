import logging

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.apps.tasks.models import Category, Task
from src.apps.tasks.schemas import TaskIn
from src.core.db import engine

logger: logging.Logger = logging.getLogger(__name__)


class TaskRepository:
    def __init__(self, session: async_sessionmaker) -> None:
        self.db_session: async_sessionmaker = session

    async def create(self, user_id: int, payload: TaskIn) -> Task:
        async with self.db_session() as session:
            statement = (
                insert(Task)
                .values(
                    user_id=user_id,
                    **payload.model_dump(),
                )
                .returning(Task)
            )
            logger.debug(statement.compile(engine, compile_kwargs={"literal_binds": True}))
            result = await session.execute(statement)
            task = result.scalar()
            await session.commit()
            logger.debug(task)
            return task

    async def get_all(self) -> list[Task]:
        async with self.db_session() as session:
            statement = select(Task)
            logger.debug(statement.compile(engine, compile_kwargs={"literal_binds": True}))
            result = await session.execute(statement)
            return list(result.scalars().all())

    async def get(self, task_id: int) -> Task:
        async with self.db_session() as session:
            statement = select(Task).where(Task.id == task_id)
            logger.debug(statement.compile(engine, compile_kwargs={"literal_binds": True}))
            result = await session.execute(statement)
            return result.scalar()

    async def get_task_by_user(self, user_id: int, task_id: int) -> Task:
        async with self.db_session() as session:
            statement = select(Task).where(
                Task.user_id == user_id,
                Task.id == task_id,
            )
            logger.debug(statement.compile(engine, compile_kwargs={"literal_binds": True}))
            result = await session.execute(statement)
            return result.scalar()

    async def get_tasks_by_category_name(self, category_name: str) -> list[Task]:
        with self.db_session() as session:
            query = (
                select(Task)
                .join(Category, Task.category_id == Category.id)
                .where(Category.name == category_name)
            )
            logger.debug(query.compile(engine, compile_kwargs={"literal_binds": True}))
            return session.execute(query).scalars().all()

    async def update(self, user_id: int, task_id: int, payload: TaskIn) -> Task:
        async with self.db_session() as session:
            query = (
                update(Task)
                .where(
                    Task.id == task_id,
                    Task.user_id == user_id,
                )
                .values(
                    **payload.model_dump(),
                )
                .returning(Task.id)
            )
            logger.debug(query.compile(engine, compile_kwargs={"literal_binds": True}))
            result = await session.execute(query)
            task_id = result.scalar()
            await session.commit()
            return await self.get(task_id)

    async def delete(self, task_id: int):
        async with self.db_session() as session:
            statement = delete(Task).where(Task.id == task_id)
            logger.debug(statement.compile(engine, compile_kwargs={"literal_binds": True}))
            await session.execute(statement)
            await session.commit()
