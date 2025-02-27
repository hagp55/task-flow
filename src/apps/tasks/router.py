import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.apps.tasks.schemas import TaskIn, TaskOut
from src.apps.tasks.services import TasksService
from src.core.pagination import Pagination, pagination_params
from src.dependencies import get_request_user_id, get_tasks_service
from src.exceptions import ProjectNotFoundException, TaskAlreadyExistsException, TaskNotFoundException

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "",
    name="Create a new task 📝",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    payload: TaskIn,
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: Annotated[int, Depends(get_request_user_id)],
) -> TaskOut:
    """
    Create a new task with the following parameters:

    - **name**: the name of the task (must be between 2 and 500 characters).
    - **project_id**: optional project ID to associate the task (if provided, it should be a positive integer).
    - **priority**: the priority of the task (defaults to `low`). You can choose from `low`, `medium`, or `high`.
    - **status**: the status of the task (defaults to `pending`). Options include `pending`, `progress`, or `completed`.
    """
    try:
        return await task_service.create(user_id=user_id, payload=payload)
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.detail),
        )
    except TaskAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e.detail),
        )


@router.get(
    "",
    name="Get tasks 📖",
    response_model=list[TaskOut],
    status_code=status.HTTP_200_OK,
)
async def get_tasks(
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: Annotated[int, Depends(get_request_user_id)],
    pagination: Annotated[Pagination, Depends(pagination_params)],
) -> list[TaskOut]:
    """
    Get a list of all tasks for the authenticated user:

    - This endpoint returns all tasks that are assigned to the authenticated user.
    - The response includes a list of tasks with their attributes such as:
        - **name**: The name of the task.
        - **priority**: The priority level of the task.
        - **status**: The current status of the task.
        - **created_at**: The timestamp of when the task was created.
        - **updated_at**: The timestamp of when the task was last updated.

    If the user has no tasks, an empty list will be returned.
    """
    return await task_service.get_all(user_id=user_id, pagination=pagination)


@router.get(
    "/{task_id}",
    name="Get a specific task by its ID 📖",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
)
async def get_task(
    task_id: int,
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: Annotated[int, Depends(get_request_user_id)],
) -> TaskOut:
    """
    Get a specific task by its ID for the authenticated user:

    - This endpoint retrieves a single task based on the provided task ID.
    - The response will include the task attributes such as:
        - **name**: The name of the task.
        - **priority**: The priority level of the task.
        - **status**: The current status of the task.
        - **created_at**: The timestamp of when the task was created.
        - **updated_at**: The timestamp of when the task was last updated.

    If the task does not belong to the authenticated user or does not exist, a 404 error will be returned.
    """
    try:
        return await task_service.get(user_id=user_id, task_id=task_id)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.detail),
        )


@router.put(
    "/{task_id}",
    name="Update a task with the provided data ✏",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_id: int,
    payload: TaskIn,
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: Annotated[int, Depends(get_request_user_id)],
) -> TaskOut:
    """
    Update an existing task with new details:

    - **name**: the name of the task.
    - **priority**: optional new priority level of the task. You can choose from `low`, `medium`, `high`.
    - **status**: optional new status of the task. You can choose from `pending`, `progress`, or `completed`.
    """
    try:
        return await task_service.update(
            user_id=user_id,
            task_id=task_id,
            payload=payload,
        )
    except (TaskNotFoundException, ProjectNotFoundException, TaskAlreadyExistsException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.detail),
        )


@router.delete(
    "/{task_id}",
    name="Delete task 🗑️",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: Annotated[int, Depends(get_request_user_id)],
) -> None:
    """
    Delete a task by its ID:

    - **task_id**: The ID of the task to be deleted. This task must belong to the user.

    If the task is not found or does not belong to the user, a 404 error will be raised.
    """
    try:
        await task_service.delete(user_id=user_id, task_id=task_id)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.detail),
        )
