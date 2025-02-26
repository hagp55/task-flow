import logging
from dataclasses import dataclass

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.projects.models import Project

logger = logging.getLogger(__name__)


@dataclass
class ProjectRepository:
    session: AsyncSession

    async def get_all(
        self,
        user_id: int,
        order,
        page: int,
        per_page: int,
    ) -> list[Project]:
        result = await self.session.execute(
            select(Project)
            .where(Project.user_id == user_id)
            .limit(per_page)
            .offset(page - 1 if page == 1 else (page - 1) * per_page)
            .order_by(
                order(Project.updated_at),
            ),
        )
        return list(result.scalars().unique())

    async def get(self, *, user_id: int, project_id: int) -> Project | None:
        return await self.session.scalar(
            select(Project).where(
                Project.id == project_id,
                Project.user_id == user_id,
            )
        )

    async def get_by_name(self, *, user_id: int, name: str) -> Project | None:
        return await self.session.scalar(
            select(Project).where(
                Project.name == name,
                Project.user_id == user_id,
            )
        )

    async def create(self, *, user_id: int, payload: dict) -> Project | None:
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

    async def update(self, *, project_id: int, payload: dict) -> Project | None:
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

    async def delete(self, *, project_id: int) -> None:
        await self.session.execute(delete(Project).where(Project.id == project_id))
        await self.session.commit()
