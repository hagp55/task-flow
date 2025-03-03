import os

import pytest


@pytest.fixture(scope="function")
def alembic_config() -> None:
    """Change ENVIRONMENT to tests for ALEMBIC .ENV"""
    os.environ["ENVIRONMENT"] = "tests"
