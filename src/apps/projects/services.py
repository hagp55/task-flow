import logging
from dataclasses import dataclass

from src.apps.projects.models import Project
from src.apps.projects.repository import ProjectRepository
from src.apps.projects.schemas import ProjectIn, ProjectOut
from src.exceptions import ProjectNotFoundException

logger = logging.getLogger(__name__)


@dataclass
class ProjectService:
    project_repository: ProjectRepository

    async def create(self, *, user_id: int, payload: ProjectIn) -> ProjectOut:
        project: Project | None = await self.project_repository.create(
            user_id=user_id,
            payload=payload.model_dump(),
        )
        return ProjectOut.model_validate(project)

    async def get_all(self, user_id: int) -> list[ProjectOut]:
        projects: list[Project] = await self.project_repository.get_all(user_id=user_id)
        return [ProjectOut.model_validate(project) for project in projects]

    async def get(self, *, user_id: int, project_id: int) -> ProjectOut:
        project: Project | None = await self.project_repository.get(
            user_id=user_id,
            project_id=project_id,
        )
        if project is None:
            raise ProjectNotFoundException
        return ProjectOut.model_validate(project)

    async def update(self, *, user_id: int, project_id: int, payload: ProjectIn) -> ProjectOut:
        project: Project | None = await self.project_repository.get(
            user_id=user_id,
            project_id=project_id,
        )
        if project is None:
            raise ProjectNotFoundException
        updated_project: Project | None = await self.project_repository.update(
            project_id=project.id,
            payload=payload.model_dump(),
        )
        return ProjectOut.model_validate(updated_project)

    async def delete(self, *, user_id: int, project_id: int) -> None:
        project: Project | None = await self.project_repository.get(
            user_id=user_id,
            project_id=project_id,
        )
        if project is None:
            raise ProjectNotFoundException
        await self.project_repository.delete(project_id=project_id)
