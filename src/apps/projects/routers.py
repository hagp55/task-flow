import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status

from src.apps.projects.schemas import ProjectIn, ProjectOut
from src.apps.projects.services import ProjectService
from src.core.pagination import Pagination, pagination_params
from src.dependencies import get_project_service, get_request_user_id
from src.exceptions import ProjectAlreadyExistsException, ProjectNotFoundException

router = APIRouter()


@router.post(
    "",
    name="Create a new project",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    payload: ProjectIn,
    user_id: Annotated[uuid.UUID, Depends(get_request_user_id)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectOut:
    """
    Create a new project for the authenticated user.

    **Request**:
    - **name**: The name of the project (must be between 2 and 250 characters).

    **Responses:**
    - `201 Created`: The project was successfully created, and the response will contain the project details.
    - `409 Conflict`: If a project with the same name already exists for the user.

    This endpoint creates a new project with the specified name and associates it with the authenticated user.
      If the project already exists, a `409 Conflict` error will be returned.
    """
    try:
        return await project_service.create(user_id=user_id, payload=payload)
    except ProjectAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e.detail),
        )


@router.get(
    "",
    name="Get projects",
    response_model=list[ProjectOut],
    status_code=status.HTTP_200_OK,
)
async def get_projects(
    user_id: Annotated[uuid.UUID, Depends(get_request_user_id)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
    pagination: Annotated[Pagination, Depends(pagination_params)],
) -> list[ProjectOut]:
    """
    Get a list of all projects associated with the authenticated user.

    - This endpoint get all projects that belong to the authenticated user.
    - The response will contain a list of project objects with their details, including:
        - **id**: The unique ID of the project.
        - **name**: The name of the project.
        - **created_at**: The timestamp of when the project was created.
        - **updated_at**: The timestamp of when the project was last updated.
        - **tasks**: A list of tasks associated with the project (if any).

    - **Pagination**: The response will be paginated based on the provided pagination parameters,
      allowing users to fetch the projects in chunks.

    **Responses:**
    - `200 OK`: A list of projects associated with the authenticated user.
    """
    return await project_service.get_all(
        user_id=user_id,
        pagination=pagination,
    )


@router.get(
    "/{project_id}",
    name="Get project",
    response_model=ProjectOut,
    status_code=status.HTTP_200_OK,
)
async def get_project(
    project_id: Annotated[uuid.UUID, Path()],
    user_id: Annotated[uuid.UUID, Depends(get_request_user_id)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectOut:
    """
    Get the details of a specific project by its ID for the authenticated user.

    **Request**:
    - **project_id**: The unique ID of the project to be fetched (must be a uuid).

    **Response**:
    - Returns the project details, including:
        - **id**: The unique ID of the project.
        - **name**: The name of the project.
        - **created_at**: The timestamp of when the project was created.
        - **updated_at**: The timestamp of when the project was last updated.
        - **tasks**: A list of tasks associated with the project (if any).

    **Errors**:
    - `404 Not Found`: If the project does not exist or does not belong to the authenticated user.

    """
    try:
        return await project_service.get(user_id=user_id, project_id=project_id)
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.detail),
        )


@router.put(
    "/{project_id}",
    name="Update project",
    response_model=ProjectOut,
    status_code=status.HTTP_200_OK,
)
async def update_project(
    project_id: Annotated[uuid.UUID, Path()],
    payload: ProjectIn,
    user_id: Annotated[uuid.UUID, Depends(get_request_user_id)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectOut:
    """
    Update the details of an existing project for the authenticated user.

    **Request**:
    - **project_id**: The ID of the project to be updated (must be a uuid).
    - **payload**: Data to update the project, including the project name.

    **Response**:
    - Returns the updated project details, including:
        - **id**: The unique ID of the project (must be a uuid).
        - **name**: The updated name of the project.
        - **created_at**: The timestamp of when the project was created.
        - **updated_at**: The timestamp of when the project was last updated.
        - **tasks**: A list of tasks associated with the project (if any).

    **Errors**:
    - `404 Not Found`: If the project does not exist or does not belong to the authenticated user.
    """
    try:
        return await project_service.update(
            user_id=user_id,
            project_id=project_id,
            payload=payload,
        )
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.detail),
        )


@router.delete(
    "/{project_id}",
    name="Delete project",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: Annotated[uuid.UUID, Path()],
    user_id: Annotated[uuid.UUID, Depends(get_request_user_id)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> None:
    """
    Delete a specific project by its ID for the authenticated user.

    **Request**:
    - **project_id**: The ID of the project to be deleted (must be a uuid).

    **Response**:
    - `204 No Content`: The project was successfully deleted, and no content is returned.

    **Errors**:
    - `404 Not Found`: If the project does not exist or does not belong to the authenticated user.
    """
    try:
        await project_service.delete(user_id=user_id, project_id=project_id)
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.detail),
        )
