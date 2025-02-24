from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status

from src.apps.projects.schemas import ProjectIn, ProjectOut
from src.apps.projects.services import ProjectService
from src.core.dependencies import get_project_service, get_request_user_id
from src.exceptions import ProjectNotFoundException

router = APIRouter()


@router.post(
    "/",
    name="Create a new project 📌 ",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    payload: ProjectIn,
    user_id: Annotated[int, Depends(get_request_user_id)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectOut:
    return await project_service.create(user_id=user_id, payload=payload)


@router.get(
    "/",
    name="Get projects 📖 ",
    response_model=list[ProjectOut],
    status_code=status.HTTP_200_OK,
)
async def get_projects(
    user_id: Annotated[int, Depends(get_request_user_id)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> list[ProjectOut]:
    return await project_service.get_all(user_id=user_id)


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
    name="Delete project 🗑️",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: Annotated[int, Path(ge=1)],
    user_id: Annotated[int, Depends(get_request_user_id)],
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> None:
    try:
        await project_service.delete(user_id=user_id, project_id=project_id)
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.detail),
        )
