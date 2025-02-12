from src.apps.tasks.repositories import TaskRepository
from src.core.db import session_factory


def get_tasks_repository() -> TaskRepository:
    return TaskRepository(session_factory)
