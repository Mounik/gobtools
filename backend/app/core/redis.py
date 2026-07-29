from redis.asyncio import Redis

from app.core.config import settings

redis_client: Redis | None = None


async def get_redis() -> Redis:
    global redis_client
    if redis_client is None:
        redis_client = Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT
        )
    return redis_client


async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.aclose()
        redis_client = None
