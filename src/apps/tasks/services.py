import logging
import uuid
from dataclasses import dataclass

from sqlalchemy import asc, desc

from src.apps.projects.models import Project
from src.apps.projects.repository import ProjectRepository
from src.apps.tasks.cache_repositories import CacheTasks
from src.apps.tasks.models import Task
from src.apps.tasks.repository import TaskRepository
from src.apps.tasks.schemas import TaskIn, TaskOut
from src.core.pagination import Pagination, SortEnum
from src.exceptions import ProjectNotFoundException, TaskAlreadyExistsException, TaskNotFoundException

logger = logging.getLogger(__name__)


@dataclass
class TasksService:
    task_repository: TaskRepository
    cache_task_repository: CacheTasks
    project_repository: ProjectRepository

    async def get_all(self, *, user_id: uuid.UUID, pagination: Pagination) -> list[TaskOut]:
        order = desc if pagination.order == SortEnum.DESC else asc
        tasks: list[Task] = await self.task_repository.get_all(
            user_id=user_id,
            order=order,
            page=pagination.page,
            per_page=pagination.perPage,
        )
        return [TaskOut.model_validate(task) for task in tasks]

    async def get(self, user_id: uuid.UUID, task_id: uuid.UUID) -> TaskOut:
        task: Task | None = await self.task_repository.get(
            task_id=task_id,
            user_id=user_id,
        )
        if task:
            return TaskOut.model_validate(task)
        raise TaskNotFoundException

    async def create(self, *, user_id: uuid.UUID, payload: TaskIn) -> TaskOut:
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
            return TaskOut.model_validate(task)
        raise TaskAlreadyExistsException

    async def update(self, *, user_id: uuid.UUID, task_id: uuid.UUID, payload: TaskIn) -> TaskOut:
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
        if task:
            if (
                payload.name == task.name
                and payload.priority == task.priority
                and payload.status == task.status
                and (payload.project_id == task.project_id or (payload.project_id is None and task.project_id is None))
            ):
                return TaskOut.model_validate(task)
            updated_task = await self.task_repository.update(
                task_id=task_id,
                payload=payload.model_dump(exclude_unset=True),
            )
            return TaskOut.model_validate(updated_task)
        raise TaskNotFoundException

    async def delete(self, *, user_id: uuid.UUID, task_id: uuid.UUID) -> None:
        task: Task | None = await self.task_repository.get(task_id=task_id, user_id=user_id)
        if task:
            await self.task_repository.delete(user_id=user_id, task_id=task_id)
            return
        raise TaskNotFoundException
