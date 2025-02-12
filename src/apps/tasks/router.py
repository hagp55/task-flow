import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from src.apps.tasks.models import Task
from src.apps.tasks.repositories import TaskRepository
from src.apps.tasks.schemas import TaskIn, TaskOut
from src.dependencies import get_tasks_repository

__all__ = ("router",)


router = APIRouter(prefix="/tasks", tags=["Tasks"])
logger = logging.getLogger(__name__)


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskIn,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> Task:
    return task_repository.create(payload)


@router.get("", response_model=list[TaskOut], status_code=status.HTTP_200_OK)
async def get_tasks(
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> list[Task]:
    return task_repository.get_all()


@router.get("/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def get_task(
    task_id: int,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> Task:
    return task_repository.get(task_id)


@router.patch("/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: int,
    payload: TaskIn,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> Task:
    return task_repository.update(task_id, payload)


@router.delete("/{task_id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> None:
    task_repository.delete(task_id)
