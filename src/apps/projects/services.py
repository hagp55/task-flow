import logging
import uuid
from dataclasses import dataclass

from sqlalchemy import asc, desc

from src.apps.projects.models import Project
from src.apps.projects.repository import ProjectRepository
from src.apps.projects.schemas import ProjectIn, ProjectOut
from src.core.pagination import Pagination, SortEnum
from src.exceptions import ProjectAlreadyExistsException, ProjectNotFoundException

logger = logging.getLogger(__name__)


@dataclass
class ProjectService:
    project_repository: ProjectRepository

    async def create(self, *, user_id: uuid.UUID, payload: ProjectIn) -> ProjectOut:
        exists_project: Project | None = await self.project_repository.get_by_name(
            user_id=user_id,
            name=payload.name,
        )
        if not exists_project:
            project: Project | None = await self.project_repository.create(
                user_id=user_id,
                payload=payload.model_dump(),
            )
            return ProjectOut.model_validate(project)
        raise ProjectAlreadyExistsException

    async def get_all(self, user_id: uuid.UUID, pagination: Pagination) -> list[ProjectOut]:
        order = desc if pagination.order == SortEnum.DESC else asc
        projects: list[Project] = await self.project_repository.get_all(
            user_id=user_id,
            order=order,
            page=pagination.page,
            per_page=pagination.perPage,
        )
        return [ProjectOut.model_validate(project) for project in projects]

    async def get(self, *, user_id: uuid.UUID, project_id: uuid.UUID) -> ProjectOut:
        project: Project | None = await self.project_repository.get(
            user_id=user_id,
            project_id=project_id,
        )
        if project is None:
            raise ProjectNotFoundException
        return ProjectOut.model_validate(project)

    async def update(self, *, user_id: uuid.UUID, project_id: uuid.UUID, payload: ProjectIn) -> ProjectOut:
        project: Project | None = await self.project_repository.get(
            user_id=user_id,
            project_id=project_id,
        )
        if project:
            exists_project: Project | None = await self.project_repository.get_by_name(
                user_id=user_id,
                name=payload.name,
            )
            if not exists_project:
                updated_project: Project | None = await self.project_repository.update(
                    project_id=project.id,
                    payload=payload.model_dump(),
                )
                return ProjectOut.model_validate(updated_project)
            raise ProjectAlreadyExistsException
        raise ProjectNotFoundException

    async def delete(self, *, user_id: uuid.UUID, project_id: uuid.UUID) -> None:
        project: Project | None = await self.project_repository.get(
            user_id=user_id,
            project_id=project_id,
        )
        if project is None:
            raise ProjectNotFoundException
        await self.project_repository.delete(project_id=project_id)
