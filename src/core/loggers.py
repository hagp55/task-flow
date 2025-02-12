import logging
import logging.config
from pathlib import Path

import yaml

from src.core.settings import settings

__all__ = ("set_logging",)


def set_logging() -> None:
    log_files: dict[str, str] = {
        "dev": "logging.dev.yaml",
        "prod": "logging.prod.yaml",
    }

    logger_config: Path = settings.BASE_DIR / log_files.get(settings.ENVIRONMENT, "")
    if not logger_config.exists():
        print(f"Отсутствуют конфигурационные файлы: {logger_config}")
        exit(1)
    with open(logger_config, "rt") as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)
