import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.core.db import Base
from src.core.settings import db
from tests.db_connector import TestingSessionLocal, app, test_engine

engine: AsyncEngine = create_async_engine(
    url=db.ASYNC_DNS_DB,
    echo=db.SQL_REQUESTS_SHOW_IN_CONSOLE,
    pool_pre_ping=True,
    isolation_level="AUTOCOMMIT",
)


@pytest.fixture(scope="session", autouse=True)
async def init_database():
    async with engine.begin() as conn:
        await conn.exec_driver_sql(f"DROP DATABASE IF EXISTS TEST_{db.POSTGRES_DB} WITH (FORCE)")
        await conn.exec_driver_sql(f"CREATE DATABASE TEST_{db.POSTGRES_DB}")
    yield
    async with engine.begin() as conn:
        await conn.exec_driver_sql(f"DROP DATABASE IF EXISTS TEST_{db.POSTGRES_DB} WITH (FORCE)")


@pytest.fixture(scope="function", autouse=True)
async def init_tables():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def session():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as async_client:
        yield async_client
