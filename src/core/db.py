import uuid
from typing import Annotated

from sqlalchemy import Boolean, MetaData, String
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column

from src.core.settings import db
from src.core.utils.db import camel_to_snake, singular_to_plural

engine: AsyncEngine = create_async_engine(
    url=db.ASYNC_DNS_DB,
    echo=db.SQL_REQUESTS_SHOW_IN_CONSOLE,
    pool_pre_ping=True,
    isolation_level="AUTOCOMMIT",
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


# Types for SQLALCHEMY
uuid_id = Annotated[str, mapped_column(primary_key=True, default=str(uuid.uuid4()))]

str_100 = Annotated[str, mapped_column(String(length=100))]
str_150 = Annotated[str, mapped_column(String(length=150))]
str_200 = Annotated[str, mapped_column(String(length=200))]
str_250 = Annotated[str, mapped_column(String(length=250))]
str_500 = Annotated[str, mapped_column(String(length=500))]

str_100_or_none = Annotated[str | None, mapped_column(String(length=100))]
str_150_or_none = Annotated[str | None, mapped_column(String(length=150))]
str_200_or_none = Annotated[str | None, mapped_column(String(length=200))]
str_250_or_none = Annotated[str | None, mapped_column(String(length=250))]
str_500_or_none = Annotated[str | None, mapped_column(String(length=500))]

uniq_str_100 = Annotated[str, mapped_column(String(length=100), unique=True)]
uniq_str_150 = Annotated[str, mapped_column(String(length=150), unique=True)]
uniq_str_128 = Annotated[str, mapped_column(String(length=200), unique=True)]
uniq_str_250 = Annotated[str, mapped_column(String(length=250), unique=True)]
uniq_str_500 = Annotated[str, mapped_column(String(length=500), unique=True)]

uniq_str_100_or_none = Annotated[str | None, mapped_column(String(length=100), unique=True)]
uniq_str_150_or_none = Annotated[str | None, mapped_column(String(length=150), unique=True)]
uniq_str_200_or_none = Annotated[str | None, mapped_column(String(length=100), unique=True)]
uniq_str_250_or_none = Annotated[str | None, mapped_column(String(length=100), unique=True)]
uniq_str_500_or_none = Annotated[str | None, mapped_column(String(length=100), unique=True)]


boolean_true = Annotated[bool, mapped_column(Boolean, default=True)]
boolean_false = Annotated[bool, mapped_column(Boolean, default=False)]
