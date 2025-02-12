from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker

from src.core.settings import db
from src.core.utils.db import camel_to_snake, singular_to_plural

engine: Engine = create_engine(url=db.DNS_DB)
session_factory = sessionmaker(bind=engine)

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


def get_session():
    with session_factory() as session:
        yield session
