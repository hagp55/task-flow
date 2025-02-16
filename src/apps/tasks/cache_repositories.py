from redis import Redis

from src.apps.tasks.schemas import TaskOut


class CacheTasks:
    def __init__(self, redis: Redis) -> None:
        self.redis: Redis = redis

    async def get_all(self) -> list[TaskOut]:
        async with self.redis as redis:
            tasks_json = await redis.lrange("tasks", 0, -1)
            return [TaskOut.model_validate_json(task) for task in tasks_json]  # type: ignore

    async def create(self, tasks: list[TaskOut]) -> None:
        tasks_json: list[str] = [task.model_dump_json() for task in tasks]
        async with self.redis as redis:
            await redis.lpush("tasks", *tasks_json)

    async def delete(self):
        async with self.redis as redis:
            await redis.delete("tasks")
