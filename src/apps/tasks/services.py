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

    def get_all(self):
        if cache_tasks := self.cache_task_repository.get_all():  # type: ignore
            return cache_tasks
        tasks: list[Task] = self.task_repository.get_all()
        if tasks:
            tasks_schema: list[TaskOut] = [TaskOut.model_validate(task) for task in tasks]
            self.cache_task_repository.create(tasks_schema)
        return self.task_repository.get_all()

    def create(self, user_id: int, payload: TaskIn) -> TaskOut:
        task: Task = self.task_repository.create(user_id, payload)
        return TaskOut.model_validate(task)

    def update(self, user_id: int, task_id, payload: TaskIn) -> TaskOut:
        task: Task = self.task_repository.get_task_by_user(user_id, task_id)
        if not task:
            raise TaskNotFoundException
        task: Task = self.task_repository.update(user_id, task_id, payload)
        return TaskOut.model_validate(task)

    def delete(self, user_id: int, task_id) -> None:
        task: Task = self.task_repository.get_task_by_user(user_id, task_id)
        if not task:
            raise TaskNotFoundException
        self.task_repository.delete(task_id)
