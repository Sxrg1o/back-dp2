"""
Common dependencies for dependency injection.
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from app.core.config import settings
from app.core.database import async_session_maker


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    """Get Redis connection."""
    redis_client = redis.from_url(settings.REDIS_URL)
    try:
        yield redis_client
    finally:
        await redis_client.close()