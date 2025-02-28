import logging
from dataclasses import dataclass

from sqlalchemy import asc, desc

from src.apps.projects.models import Project
from src.apps.projects.repository import ProjectRepository
from src.apps.tasks.cache_repositories import CacheTasks
from src.apps.tasks.models import Task
from src.apps.tasks.repositories import TaskRepository
from src.apps.tasks.schemas import TaskIn, TaskOut
from src.core.pagination import Pagination, SortEnum
from src.exceptions import ProjectNotFoundException, TaskAlreadyExistsException, TaskNotFoundException

logger = logging.getLogger(__name__)


@dataclass
class TasksService:
    task_repository: TaskRepository
    cache_task_repository: CacheTasks
    project_repository: ProjectRepository

    async def get_all(self, *, user_id: int, pagination: Pagination) -> list[TaskOut]:
        # if cache_tasks := await self.cache_task_repository.get_all():  # type: ignore
        #     return cache_tasks
        # tasks: list[Task] = await self.task_repository.get_all()
        # if tasks:
        #     tasks_schema: list[TaskOut] = [TaskOut.model_validate(task) for task in tasks]
        # await self.cache_task_repository.create(tasks_schema)
        order = desc if pagination.order == SortEnum.DESC else asc
        tasks: list[Task] = await self.task_repository.get_all(
            user_id=user_id,
            order=order,
            page=pagination.page,
            per_page=pagination.perPage,
        )
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
        if payload.project_id:
            exists_project: Project | None = await self.project_repository.get(
                user_id=user_id,
                project_id=payload.project_id,
            )
            if not exists_project:
                raise ProjectNotFoundException
        exists_task_name: Task | None = await self.task_repository.get_by_name(
            user_id=user_id,
            name=payload.name,
        )
        if not exists_task_name:
            task: Task | None = await self.task_repository.create(
                user_id=user_id,
                payload=payload.model_dump(),
            )
            # await self.cache_task_repository.delete()
            return TaskOut.model_validate(task)
        raise TaskAlreadyExistsException

    async def update(self, *, user_id: int, task_id, payload: TaskIn) -> TaskOut:
        if payload.project_id:
            exists_project: Project | None = await self.project_repository.get(
                user_id=user_id,
                project_id=payload.project_id,
            )
            if not exists_project:
                raise ProjectNotFoundException
        task: Task | None = await self.task_repository.get(
            task_id=task_id,
            user_id=user_id,
        )
        if not task:
            raise TaskNotFoundException
        exists_task_name: Task | None = await self.task_repository.get_by_name(
            user_id=user_id,
            name=payload.name,
        )
        if exists_task_name:
            raise TaskAlreadyExistsException
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
