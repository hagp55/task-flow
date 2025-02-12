from dataclasses import dataclass

from src.apps.tasks.cache_repositories import CacheTasks
from src.apps.tasks.models import Task
from src.apps.tasks.repositories import TaskRepository
from src.apps.tasks.schemas import TaskOut


@dataclass
class TasksService:
    task_repository: TaskRepository
    cache_task_repository: CacheTasks

    def get_all(self):
        if cache_tasks := self.cache_task_repository.get_all():  # type: ignore
            return cache_tasks
        tasks: list[Task] = self.task_repository.get_all()
        tasks_schema: list[TaskOut] = [TaskOut.model_validate(task) for task in tasks]
        self.cache_task_repository.create(tasks_schema)
        return self.task_repository.get_all()
