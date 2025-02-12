import sqlite3
from pathlib import Path

from src.core.settings import settings

db_path: Path = settings.BASE_DIR / f"src/{settings.SQLITE_DB_NAME}"


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(db_path)
