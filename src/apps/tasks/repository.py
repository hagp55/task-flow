import logging
import uuid
from dataclasses import dataclass

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.tasks.models import Task

logger: logging.Logger = logging.getLogger(__name__)


@dataclass
class TaskRepository:
    session: AsyncSession

    async def create(self, *, user_id: uuid.UUID, payload: dict) -> Task | None:
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

    async def get_all(
        self,
        user_id: uuid.UUID,
        order,
        page: int,
        per_page: int,
    ) -> list[Task]:
        result = await self.session.execute(
            select(Task)
            .where(Task.user_id == user_id)
            .limit(per_page)
            .offset(page - 1 if page == 1 else (page - 1) * per_page)
            .order_by(
                order(Task.created_at),
            ),
        )
        return list(result.scalars().unique())

    async def get(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Task | None:
        return await self.session.scalar(
            select(
                Task,
            ).where(Task.id == task_id, Task.user_id == user_id),
        )

    async def get_by_name(self, *, user_id: uuid.UUID, name: str) -> Task | None:
        return await self.session.scalar(
            select(
                Task,
            ).where(Task.user_id == user_id, Task.name == name),
        )

    async def update(self, *, task_id: uuid.UUID, payload: dict) -> Task | None:
        task: Task | None = (
            await self.session.execute(
                update(Task)
                .where(
                    Task.id == task_id,
                )
                .values(**payload)
                .returning(Task)
            )
        ).scalar()
        await self.session.commit()
        return task

    async def delete(self, *, user_id: uuid.UUID, task_id: uuid.UUID) -> None:
        await self.session.execute(
            delete(
                Task,
            ).where(Task.id == task_id, Task.user_id == user_id)
        )
        await self.session.commit()
