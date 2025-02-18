from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from src.core.settings import db

engine: AsyncEngine = create_async_engine(
    url=db.DNS_TEST_DB,
    pool_pre_ping=True,
    poolclass=NullPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    expire_on_commit=False,
    future=True,
    autoflush=False,
)
