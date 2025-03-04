import logging
import uuid
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
    name="Create a new task",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    payload: TaskIn,
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: Annotated[uuid.UUID, Depends(get_request_user_id)],
) -> TaskOut:
    """
    Create a new task for the authenticated user with the following parameters:

    **Request**:
    - **name**: The name of the task (must be between 2 and 500 characters).
    - **project_id**: Optional project ID to associate the task (if provided, it must be a uuid).
    - **priority**: The priority of the task (defaults to `low`). You can choose from `low`, `medium`, or `high`.
    - **status**: The status of the task (defaults to `pending`). Options include `pending`, `progress`, or `completed`.

    **Responses:**
    - `201 Created`: Task successfully created.
    - `400 Bad Request`: Provided project does not exist.
    - `409 Conflict`: Task with the same name already exists.
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
    name="Get tasks",
    response_model=list[TaskOut],
    status_code=status.HTTP_200_OK,
)
async def get_tasks(
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: Annotated[uuid.UUID, Depends(get_request_user_id)],
    pagination: Annotated[Pagination, Depends(pagination_params)],
) -> list[TaskOut]:
    """
    Get a list of all tasks for the authenticated user.

    - This endpoint returns all tasks assigned to the authenticated user.
    - The response includes a paginated list of tasks with the following attributes:
        - **name**: The name of the task.
        - **priority**: The priority level of the task (`low`, `medium`, or `high`).
        - **status**: The current status of the task (`pending`, `progress`, or `completed`).
        - **created_at**: The timestamp of when the task was created.
        - **updated_at**: The timestamp of when the task was last updated.

    - **Pagination**: The response will be paginated based on the provided pagination parameters,
      allowing users to fetch the projects in chunks.

    **Responses:**
    - `200 OK`: Returns a list of tasks (empty list if no tasks are found).
    """
    return await task_service.get_all(user_id=user_id, pagination=pagination)


@router.get(
    "/{task_id}",
    name="Get a specific task by its ID",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
)
async def get_task(
    task_id: uuid.UUID,
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: Annotated[uuid.UUID, Depends(get_request_user_id)],
) -> TaskOut:
    """
    Get a specific task by its ID for the authenticated user.

    **Request**:
    - **task_id**: The unique ID of the task to be fetched (must be a uuid).


    **Response**:
    - Returns the task details, including:
        - **name**: The name of the task.
        - **priority**: The priority level of the task (`low`, `medium`, or `high`).
        - **status**: The current status of the task (`pending`, `progress`, or `completed`).

        - **created_at**: The timestamp when the task was created.
        - **updated_at**: The timestamp when the task was last updated.

    - If the task does not belong to the authenticated user or does not exist,
      the endpoint will return a `404 Not Found` error.

    **Responses:**
    - `200 OK`: Returns the details of the specified task.
    - `404 Not Found`: Returns an error if the task is not found or does not belong to the authenticated user.
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
    name="Update a task with the provided data",
    response_model=TaskOut,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_id: uuid.UUID,
    payload: TaskIn,
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: Annotated[uuid.UUID, Depends(get_request_user_id)],
) -> TaskOut:
    """
    Update the details of an existing task for the authenticated user.

    **Request**:
    - **task_id**: The ID of the task to be updated (must be a uuid).



    - **name**: The name of the task (between 2 and 500 characters).
    - **project_id**: The ID of the project to be updated (must be a uuid).
    - **priority**: Optional new priority level for the task. You can choose from:
        - `low`: Low priority
        - `medium`: Medium priority
        - `high`: High priority
    - **status**: Optional new status for the task. You can choose from:
        - `pending`: The task has not started yet.
        - `progress`: The task is currently being worked on.
        - `completed`: The task is finished.

    **Responses:**
    - `200 OK`: Returns the updated task details.
    - `400 Bad Request`: If the task is not found, the project is not found,
    or the task already exists with the same data.

    If the task with the given `task_id` does not exist, belongs to a different user, or any other conflict arises,
    a `400 Bad Request` error will be returned.
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
    name="Delete task",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: uuid.UUID,
    task_service: Annotated[TasksService, Depends(get_tasks_service)],
    user_id: Annotated[uuid.UUID, Depends(get_request_user_id)],
) -> None:
    """
    Delete a specific task by its ID for the authenticated user.

    **Request**:
    - **task_id**: The ID of the task to be deleted (must be a uuid).

    **Response**:
    - `204 No Content`: The task was successfully deleted, and no content is returned.

    **Errors**:
    - `404 Not Found`: If the task does not exist or does not belong to the authenticated user.
    """
    try:
        await task_service.delete(user_id=user_id, task_id=task_id)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.detail),
        )
