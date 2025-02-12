from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

config = SettingsConfigDict(
    extra="ignore",
    case_sensitive=False,
    env_ignore_empty=True,
    env_file_encoding="utf-8",
    env_file=Path(__file__).parents[2] / ".env",
)


class Settings(BaseSettings):
    model_config = config

    BASE_DIR: Path = Path(__file__).parents[2]
    GOOGLE_TOKEN_ID: str
    SECRET_KEY: str
    DEBUG: bool = False
    SQLITE_DB_NAME: str = "db.sqlite3"
    ENVIRONMENT: Literal["dev", "prod", "tests"] = "dev"


class Cache(BaseSettings):
    model_config = config
    CACHE_HOST: str = "0.0.0.0"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0


class DB(BaseSettings):
    model_config = config

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    SYNC_PROVIDER: str = "postgresql+psycopg2"

    @property
    def DNS_DB(self) -> str:
        return f"{self.SYNC_PROVIDER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def DNS_TEST_DB(self) -> str:
        return f"{self.SYNC_PROVIDER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/test_{self.POSTGRES_DB}"


def get_settings() -> Settings:
    return Settings()  # type: ignore


def get_db_settings() -> Settings:
    return DB()  # type: ignore


def get_cache_settings() -> Settings:
    return Cache()  # type: ignore


settings: Settings = get_settings()
db: DB = get_db_settings()  # type: ignore
cache: Cache = get_cache_settings()  # type: ignore
