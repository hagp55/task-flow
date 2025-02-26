pytest_plugins: list[str] = [
    "tests.db_connector",
    "tests.fixtures.infrastructure",
    "tests.fixtures.alembic",
    "tests.fixtures.users.user_fixture",
]
