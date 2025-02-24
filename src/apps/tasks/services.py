import logging
from dataclasses import dataclass

from src.apps.tasks.cache_repositories import CacheTasks
from src.apps.tasks.models import Task
from src.apps.tasks.repositories import TaskRepository
from src.apps.tasks.schemas import TaskIn, TaskOut
from src.exceptions import TaskNotFoundException

logger = logging.getLogger(__name__)


@dataclass
class TasksService:
    task_repository: TaskRepository
    cache_task_repository: CacheTasks

    async def get_all(self, *, user_id: int) -> list[TaskOut]:
        # if cache_tasks := await self.cache_task_repository.get_all():  # type: ignore
        #     return cache_tasks
        # tasks: list[Task] = await self.task_repository.get_all()
        # if tasks:
        #     tasks_schema: list[TaskOut] = [TaskOut.model_validate(task) for task in tasks]
        # await self.cache_task_repository.create(tasks_schema)
        tasks: list[Task] = await self.task_repository.get_all(user_id=user_id)
        return [TaskOut.model_validate(task) for task in tasks]

    async def get(self, user_id: int, task_id: int) -> TaskOut:
        task: Task | None = await self.task_repository.get(
            task_id=task_id,
            user_id=user_id,
        )
        if not task:
            raise TaskNotFoundException
        return TaskOut.model_validate(task)

    async def create(self, *, user_id: int, payload: TaskIn) -> TaskOut:
        task: Task | None = await self.task_repository.create(
            user_id=user_id,
            payload=payload.model_dump(),
        )
        # await self.cache_task_repository.delete()
        return TaskOut.model_validate(task)

    async def update(self, *, user_id: int, task_id, payload: TaskIn) -> TaskOut:
        task: Task | None = await self.task_repository.get(
            task_id=task_id,
            user_id=user_id,
        )
        if not task:
            raise TaskNotFoundException
        task = await self.task_repository.update(
            user_id=user_id,
            task_id=task_id,
            payload=payload.model_dump(),
        )
        return TaskOut.model_validate(task)

    async def delete(self, *, user_id: int, task_id) -> None:
        task: Task | None = await self.task_repository.get(
            task_id=task_id,
            user_id=user_id,
        )
        if not task:
            raise TaskNotFoundException
        await self.task_repository.delete(
            user_id=user_id,
            task_id=task_id,
        )
