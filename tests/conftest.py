pytest_plugins: list[str] = [
    "tests.db_connector",
    "tests.fixtures.infrastructure",
    "tests.fixtures.alembic",
    "tests.fixtures.users.user_fixtures",
    "tests.fixtures.projects.project_fixtures",
    "tests.fixtures.tasks.task_fixtures",
]
