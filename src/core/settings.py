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
    DEBUG: bool = False
    APP_PORT: int = 8000
    APP_HOST: str = "localhost"
    SECRET_KEY: str
    ENVIRONMENT: Literal["dev", "prod", "tests"] = "dev"

    # JTW TOKEN
    JWT_UPDATE_TIME: int = 24
    JWT_SECRET_KEY: str = "your_secret_key"
    JWT_ALGORITHM: str = "HS256"

    # OAUTH
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""
    GOOGLE_TOKEN_URL: str = "https://accounts.google.com/o/oauth2/token"

    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_REDIRECT_URI: str
    YANDEX_TOKEN_URL: str = "https://oauth.yandex.ru/token"

    @property
    def GOOGLE_REDIRECT_URL(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"

    @property
    def YANDEX_REDIRECT_URL(self) -> str:
        return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&force_confirm=yes"


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
    SQL_REQUESTS_SHOW_IN_CONSOLE: bool = False

    SYNC_PROVIDER: str = "postgresql+psycopg2"
    ASYNC_PROVIDER: str = "postgresql+asyncpg"

    @property
    def DNS_DB(self) -> str:
        return f"{self.SYNC_PROVIDER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def ASYNC_DNS_DB(self) -> str:
        return f"{self.ASYNC_PROVIDER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def DNS_TEST_DB(self) -> str:
        return f"{self.ASYNC_PROVIDER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/test_{self.POSTGRES_DB}"


def get_settings() -> Settings:
    return Settings()  # type: ignore


def get_db_settings() -> Settings:
    return DB()  # type: ignore


def get_cache_settings() -> Settings:
    return Cache()  # type: ignore


settings: Settings = get_settings()
db: DB = get_db_settings()  # type: ignore
cache: Cache = get_cache_settings()  # type: ignore
