import pytest

from src.core.db import Base
from tests.db_connector import TestingSessionLocal, engine


@pytest.fixture(scope="function", autouse=True)
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def session():
    async with TestingSessionLocal() as session:
        yield session
