import sqlite3

from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker

from src.core.settings import settings
from src.core.utils import camel_to_snake, singular_to_plural

db_path = f"sqlite:///{settings.BASE_DIR / f'src/{settings.SQLITE_DB_NAME}'}"


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(db_path)


engine: Engine = create_engine(db_path)
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
