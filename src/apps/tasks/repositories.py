import logging
from dataclasses import dataclass

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.tasks.models import Task

logger: logging.Logger = logging.getLogger(__name__)


@dataclass
class TaskRepository:
    session: AsyncSession

    async def create(self, *, user_id: int, payload: dict) -> Task | None:
        task: Task | None = (
            await self.session.execute(
                insert(
                    Task,
                )
                .values(user_id=user_id, **payload)
                .returning(Task)
            )
        ).scalar()
        await self.session.commit()
        return task

    async def get_all(self, *, user_id: int) -> list[Task]:
        tasks = await self.session.execute(
            select(Task).where(Task.user_id == user_id),
        )

        return list(tasks.scalars().unique())

    async def get(self, task_id: int, user_id) -> Task | None:
        return await self.session.scalar(
            select(
                Task,
            ).where(Task.id == task_id, Task.user_id == user_id),
        )

    async def get_by_name(self, *, user_id: int, name: str) -> Task | None:
        return await self.session.scalar(
            select(
                Task,
            ).where(Task.user_id == user_id, Task.name == name),
        )

    async def update(self, *, user_id: int, task_id: int, payload: dict) -> Task | None:
        updated_task: Task | None = (
            await self.session.execute(
                update(
                    Task,
                )
                .where(Task.id == task_id, Task.user_id == user_id)
                .values(**payload)
                .returning(Task)
            )
        ).scalar()
        await self.session.commit()
        return updated_task

    async def delete(self, *, user_id: int, task_id: int) -> None:
        await self.session.execute(
            delete(
                Task,
            ).where(Task.id == task_id, Task.user_id == user_id)
        )
        await self.session.commit()
