from pathlib import Path

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


def get_settings() -> Settings:
    return Settings()  # type: ignore


settings: Settings = get_settings()
