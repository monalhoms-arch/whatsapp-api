import redis
from config import settings

def get_redis_client():
    """Create and return a Redis connection based on settings."""
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True # Automatically decode bytes to strings
    )

redis_client = get_redis_client()
