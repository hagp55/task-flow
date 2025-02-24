import logging
from dataclasses import dataclass

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.projects.models import Project
from src.exceptions import ProjectAlreadyExistsException

logger = logging.getLogger(__name__)


@dataclass
class ProjectRepository:
    session: AsyncSession

    async def get_all(self, user_id: int) -> list[Project]:
        result = await self.session.execute(
            select(Project).where(Project.user_id == user_id),
        )
        return list(result.scalars().unique())

    async def get(self, *, user_id: int, project_id: int) -> Project | None:
        return await self.session.scalar(
            select(Project).where(
                Project.id == project_id,
                Project.user_id == user_id,
            )
        )

    async def create(self, *, user_id: int, payload: dict) -> Project | None:
        try:
            project: Project | None = (
                await self.session.execute(
                    insert(Project)
                    .values(
                        user_id=user_id,
                        **payload,
                    )
                    .returning(Project)
                )
            ).scalar()
            await self.session.commit()
            return project
        except IntegrityError:
            raise ProjectAlreadyExistsException

    async def update(self, *, project_id: int, payload: dict) -> Project | None:
        try:
            project: Project | None = (
                await self.session.execute(
                    update(Project)
                    .where(
                        Project.id == project_id,
                    )
                    .values(**payload)
                    .returning(Project)
                )
            ).scalar()
            await self.session.commit()
            return project
        except IntegrityError:
            raise ProjectAlreadyExistsException

    async def delete(self, *, project_id: int) -> None:
        await self.session.execute(delete(Project).where(Project.id == project_id))
        await self.session.commit()
