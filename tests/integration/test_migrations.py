import pytest
from pytest_alembic import create_alembic_fixture, tests

alembic = create_alembic_fixture({"file": "alembic.ini"})


@pytest.fixture(scope="function")
async def init_tables() -> None:
    pass


def test_single_head_revision(alembic, alembic_config) -> None:
    """
    Assert that there only exists one head revision.
    """
    tests.test_single_head_revision(alembic)


def test_upgrade(alembic, alembic_config) -> None:
    """
    Assert that the revision history can be run through from base to head.
    """
    tests.test_upgrade(alembic)


def test_model_definitions_match_ddl(alembic, alembic_config) -> None:
    """
    Assert that the state of the migrations matches the state of the models describing the DDL.
    """
    tests.test_model_definitions_match_ddl(alembic)


def test_up_down_consistency(alembic, alembic_config) -> None:
    """
    Assert that all downgrades succeed.
    """
    tests.test_up_down_consistency(alembic)
