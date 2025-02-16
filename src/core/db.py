from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, declared_attr

from src.core.settings import db
from src.core.utils.db import camel_to_snake, singular_to_plural

engine: AsyncEngine = create_async_engine(
    url=db.ASYNC_DNS_DB,
    echo=db.SQL_REQUESTS_SHOW_IN_CONSOLE,
    pool_pre_ping=True,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    autocommit=False,
    expire_on_commit=False,
    future=True,
    autoflush=False,
)

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return singular_to_plural(
            camel_to_snake(
                cls.__name__,
            ),
        )


async def get_async_session():
    async with AsyncSessionFactory() as session:
        yield session
