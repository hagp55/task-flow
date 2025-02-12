from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False,
        env_ignore_empty=True,
        env_file_encoding="utf-8",
        env_file=Path(__file__).parents[2] / ".env",
    )

    BASE_DIR: Path = Path(__file__).parents[2]
    GOOGLE_TOKEN_ID: str
    SECRET_KEY: str
    DEBUG: bool = False
    SQLITE_DB_NAME: str = "db.sqlite3"
    ENVIRONMENT: Literal["dev", "prod"] = "dev"


class DB(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False,
        env_ignore_empty=True,
        env_file_encoding="utf-8",
        env_file=Path(__file__).parents[2] / ".env",
    )
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    SYNC_PROVIDER: str = "postgresql+psycopg2"

    @property
    def DNS(self) -> str:
        return f"{self.SYNC_PROVIDER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


def get_settings() -> Settings:
    return Settings()  # type: ignore


def get_db_settings() -> Settings:
    return DB()  # type: ignore


settings: Settings = get_settings()
db = get_db_settings()  # type: ignore
