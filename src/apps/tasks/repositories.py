import logging

from sqlalchemy import delete, select
from sqlalchemy.orm import sessionmaker

from src.apps.tasks.models import Category, Task
from src.apps.tasks.schemas import TaskIn
from src.core.db import engine, session_factory

logger: logging.Logger = logging.getLogger(__name__)


class TaskRepository:
    def __init__(self, session: sessionmaker) -> None:
        self.db_session: sessionmaker = session

    def get_tasks(self):
        with self.db_session() as session:
            query = select(Task)
            print(query.compile(engine, compile_kwargs={"literal_binds": True}))
            tasks = session.execute(query).scalars().all()
        return tasks

    def get_task(self, task_id: int):
        with self.db_session() as session:
            query = select(Task).where(Task.id == task_id)
            print(query.compile(engine, compile_kwargs={"literal_binds": True}))
            task = session.execute(query).scalar_one_or_none()
        return task

    def create_task(self, task: TaskIn):
        with self.db_session() as session:
            session.add(task)
            session.commit()

    def delete_task(self, task_id: int):
        with self.db_session() as session:
            query = delete(Task).where(Task.id == task_id)
            print(query.compile(engine, compile_kwargs={"literal_binds": True}))
            session.execute(query)
            session.commit()

    def get_task_by_category_name(self, category_name: str):
        with self.db_session() as session:
            query = (
                select(Task)
                .join(
                    Category,
                    Task.category_id == Category.id,
                )
                .where(Category.name == category_name)
            )
            print(query.compile(engine, compile_kwargs={"literal_binds": True}))
            tasks = session.execute(query).scalars().all()
            return tasks


def get_tasks_repository() -> TaskRepository:
    return TaskRepository(session_factory)
