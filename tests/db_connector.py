from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from src.bootstrap import app
from src.core.db import get_async_session
from src.core.settings import db

test_engine: AsyncEngine = create_async_engine(
    url=db.DNS_TEST_DB,
    pool_pre_ping=True,
    poolclass=NullPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    autocommit=False,
    expire_on_commit=False,
    future=True,
    autoflush=False,
)


async def override_get_async_session():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session
