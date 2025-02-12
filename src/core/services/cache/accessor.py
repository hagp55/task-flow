from redis import Redis

from src.core.settings import cache


def get_redis_connection() -> Redis:
    return Redis(
        host=cache.CACHE_HOST,
        port=cache.CACHE_PORT,
        db=cache.CACHE_DB,
    )
