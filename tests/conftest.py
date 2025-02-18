pytest_plugins: list[str] = [
    "tests.db_connector",
    "tests.fixtures.alembic",
    "tests.fixtures.auth.clients",
    "tests.fixtures.auth.auth_service",
    "tests.fixtures.users.users_repository",
    "tests.fixtures.users.user_model",
]
