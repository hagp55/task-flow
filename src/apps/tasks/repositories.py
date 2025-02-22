import logging

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.tasks.models import Category, Task
from src.apps.tasks.schemas import TaskIn
from src.core.db import engine

logger: logging.Logger = logging.getLogger(__name__)


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.db_session: AsyncSession = session

    async def create(self, user_id: int, payload: TaskIn) -> Task:
        query = (
            insert(Task)
            .values(
                user_id=user_id,
                **payload.model_dump(),
            )
            .returning(Task)
        )
        logger.debug(
            "Query:\n%s" % (query.compile(engine, compile_kwargs={"literal_binds": True})),
        )
        result = await self.db_session.execute(query)
        task = result.scalar()
        await self.db_session.commit()
        logger.debug(task)
        return task

    async def get_all(self) -> list[Task]:
        query = select(Task)
        logger.debug(
            "Query:\n%s" % (query.compile(engine, compile_kwargs={"literal_binds": True})),
        )
        result = await self.db_session.execute(query)
        return list(result.scalars().all())

    async def get(self, task_id: int) -> Task:
        query = select(Task).where(Task.id == task_id)
        logger.debug(
            "Query:\n%s" % (query.compile(engine, compile_kwargs={"literal_binds": True})),
        )
        result = await self.db_session.execute(query)
        return result.scalar()

    async def get_task_by_user(self, user_id: int, task_id: int) -> Task:
        query = select(Task).where(
            Task.user_id == user_id,
            Task.id == task_id,
        )
        logger.debug(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.db_session.execute(query)
        return result.scalar()

    async def get_tasks_by_category_name(self, category_name: str) -> list[Task]:
        query = (
            select(Task).join(Category, Task.category_id == Category.id).where(Category.name == category_name)
        )
        logger.debug(
            "Query:\n%s" % (query.compile(engine, compile_kwargs={"literal_binds": True})),
        )
        return self.db_session.execute(query).scalars().all()

    async def update(self, user_id: int, task_id: int, payload: TaskIn) -> Task:
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
        logger.debug(
            "Query:\n%s" % (query.compile(engine, compile_kwargs={"literal_binds": True})),
        )
        result = await self.db_session.execute(query)
        task_id = result.scalar()
        await self.db_session.commit()
        return await self.get(task_id)

    async def delete(self, task_id: int) -> None:
        query = delete(Task).where(Task.id == task_id)
        logger.debug(
            "Query:\n%s" % (query.compile(engine, compile_kwargs={"literal_binds": True})),
        )
        await self.db_session.execute(query)
        await self.db_session.commit()
