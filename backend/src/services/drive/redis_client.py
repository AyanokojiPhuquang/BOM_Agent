"""Async Redis client factory for Drive Sync services."""

import redis.asyncio as aioredis

from src.configs import SETTINGS

_redis_client: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    """Get or create a shared async Redis client.

    Reads the REDIS_URL from application settings and returns a
    reusable connection instance. The client uses hiredis for
    faster parsing when available.
    """
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            SETTINGS.redis_url,
            decode_responses=True,
        )
    return _redis_client


async def close_redis() -> None:
    """Close the Redis connection pool. Call during app shutdown."""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None
