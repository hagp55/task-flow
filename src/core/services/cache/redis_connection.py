from redis import asyncio as redis

from src.core.settings import cache


def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host=cache.CACHE_HOST,
        port=cache.CACHE_PORT,
        db=cache.CACHE_DB,
    )
