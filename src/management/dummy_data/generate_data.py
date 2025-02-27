import asyncio
import sys
from pathlib import Path

from faker import Faker
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

sys.path.append(str(Path(__file__).parents[3]))
from src.apps.auth.security import bcrypt_context
from src.apps.projects.models import Project
from src.apps.tasks.models import Task
from src.apps.users.models import User
from src.core.db import engine

fake = Faker("en_US")

local_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_user(*, session: AsyncSession) -> int:
    email = "beazley@example.com"
    user: User | None = await session.scalar(
        select(
            User,
        ).where(User.email == email)
    )
    if user is None:
        user = User(
            email="beazley@example.com",
            password=bcrypt_context.hash("Str0ngP@ssw0rd!"),
            first_name="David",
            last_name="Beazly",
        )
        session.add(user)
        await session.commit()
    return user.id


async def create_projects(*, user_id: int, count_projects: int, session: AsyncSession) -> list[int]:
    project_ids: list[int] = []
    for _ in range(count_projects):
        project = Project(
            user_id=user_id,
            name=str(fake.unique.company())[:250],
        )
        session.add(project)
        await session.flush()
        project_ids.append(project.id)
    await session.commit()
    return project_ids


async def create_tasks(*, user_id: int, project_ids: list[int], count_tasks: int, session: AsyncSession) -> None:
    for proj in project_ids:
        for _ in range(count_tasks):
            task = Task(
                user_id=user_id,
                project_id=proj,
                name=str(fake.unique.company())[:250],
                priority=fake.random_element(["low", "medium", "high"]),
                status=fake.random_element(["pending", "progress", "completed"]),
            )
            session.add(task)
        await session.commit()


async def main() -> None:
    try:
        count_projects = int(input("How much projects do you want to create? (default=25, maximum 100): "))
        count_tasks = int(input("How many tasks for each project do you want to create? (default=50, maximum 500): "))
    except ValueError:
        count_projects = 25
        count_tasks = 50
        print(f"Your data not correct, will be generate projects: {count_projects}, tasks: {count_tasks}")
    count_projects: int = count_projects if count_projects <= 100 else 100
    count_tasks: int = count_tasks if count_tasks <= 500 else 500
    try:
        async with local_session() as session:
            user_id: int = await create_user(session=session)
            project_ids: list[int] = await create_projects(
                user_id=user_id, count_projects=count_projects, session=session
            )
            await create_tasks(user_id=user_id, project_ids=project_ids, count_tasks=count_tasks, session=session)
    except (IntegrityError, SQLAlchemyError):
        print("\x1b[31m Please before generate data, drop all data from tables.\x1b[0m\n")
    else:
        print("\x1b[35m The tables were successfully filled in.\x1b[0m\n")


if __name__ == "__main__":
    asyncio.run(main())
