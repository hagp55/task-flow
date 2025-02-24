from redis import asyncio as redis

from src.core.settings import cache


def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host=cache.REDIS_HOST,
        port=cache.REDIS_PORT,
        db=cache.REDIS_DB,
    )
