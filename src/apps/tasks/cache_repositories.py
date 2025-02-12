from redis import Redis

from src.apps.tasks.schemas import TaskOut


class CacheTasks:
    def __init__(self, redis: Redis) -> None:
        self.redis: Redis = redis

    def get_all(self) -> list[TaskOut]:
        with self.redis as redis:
            tasks_json = redis.lrange("tasks", 0, -1)
            return [TaskOut.model_validate_json(task) for task in tasks_json]  # type: ignore

    def create(self, tasks: list[TaskOut]) -> None:
        tasks_json: list[str] = [task.model_dump_json() for task in tasks]
        with self.redis as redis:
            redis.lpush("tasks", *tasks_json)
