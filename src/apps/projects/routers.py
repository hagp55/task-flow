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
    name="Create a new project 📌 ",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    payload: ProjectIn,
    user_id: Annotated[int, Depends(get_request_user_id)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectOut:
    """
    Create a new project with the provided information:

    - **name**: Name of the project (must be between 2 and 250 characters).
    - **user_id**: User ID who owns the project.

    Returns the newly created project with its details.
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
    name="Get projects 📖",
    response_model=list[ProjectOut],
    status_code=status.HTTP_200_OK,
)
async def get_projects(
    user_id: Annotated[int, Depends(get_request_user_id)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
    pagination: Annotated[Pagination, Depends(pagination_params)],
) -> list[ProjectOut]:
    """
    Get a list of all projects associated with the authenticated user.

    Returns a list of project objects with their details.
    """
    return await project_service.get_all(
        user_id=user_id,
        pagination=pagination,
    )


@router.get(
    "/{project_id}",
    name="Get project 📖 ",
    response_model=ProjectOut,
    status_code=status.HTTP_200_OK,
)
async def get_project(
    project_id: Annotated[int, Path(ge=1)],
    user_id: Annotated[int, Depends(get_request_user_id)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectOut:
    """
    Get the details of a specific project by its ID.

    - **project_id**: ID of the project to be fetched.
    - **user_id**: The user ID of the authenticated user.

    Returns the details of the specified project.
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
    name="Update project ✏",
    response_model=ProjectOut,
    status_code=status.HTTP_200_OK,
)
async def update_project(
    project_id: Annotated[int, Path(ge=1)],
    payload: ProjectIn,
    user_id: Annotated[int, Depends(get_request_user_id)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectOut:
    """
    Update the details of an existing project.

    - **project_id**: ID of the project to be updated.
    - **payload**: Data to update the project (name).
    - **user_id**: The user ID of the authenticated user.

    Returns the updated project details.
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
    except ProjectAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.detail),
        )


@router.delete(
    "/{project_id}",
    name="Delete project 🗑️",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: Annotated[int, Path(ge=1)],
    user_id: Annotated[int, Depends(get_request_user_id)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> None:
    """
    Delete a specific project by its ID.

    - **project_id**: ID of the project to be deleted.
    - **user_id**: The user ID of the authenticated user.

    Returns a 204 status code if the project is successfully deleted.
    """
    try:
        await project_service.delete(user_id=user_id, project_id=project_id)
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.detail),
        )
