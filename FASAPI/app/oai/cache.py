"""
Cache utilities for external integrations.
"""
import json
from typing import Any, Optional
from datetime import datetime, timedelta

import redis.asyncio as redis

from app.core.config import settings
from app.core.logging import logger


class IntegrationCache:
    """Cache for external integration results."""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
    
    async def _get_client(self) -> redis.Redis:
        """Get Redis client."""
        if not self.redis_client:
            self.redis_client = redis.from_url(settings.REDIS_URL)
        return self.redis_client
    
    async def close(self):
        """Close Redis connection."""
        if self.redis_client:
            await self.redis_client.close()
    
    def _make_key(self, prefix: str, identifier: str) -> str:
        """Create cache key."""
        return f"integration:{prefix}:{identifier}"
    
    async def get_menu(self, restaurant_id: str) -> Optional[dict]:
        """Get cached menu data."""
        try:
            client = await self._get_client()
            key = self._make_key("menu", restaurant_id)
            
            cached_data = await client.get(key)
            if cached_data:
                logger.debug("Cache hit for menu", restaurant_id=restaurant_id)
                return json.loads(cached_data)
            
            logger.debug("Cache miss for menu", restaurant_id=restaurant_id)
            return None
            
        except Exception as e:
            logger.error("Error getting cached menu", restaurant_id=restaurant_id, error=str(e))
            return None
    
    async def set_menu(
        self,
        restaurant_id: str,
        menu_data: dict,
        ttl: Optional[int] = None
    ) -> bool:
        """Cache menu data."""
        try:
            client = await self._get_client()
            key = self._make_key("menu", restaurant_id)
            
            # Add timestamp to cached data
            cached_data = {
                "data": menu_data,
                "cached_at": datetime.utcnow().isoformat(),
            }
            
            ttl = ttl or settings.CACHE_TTL_SECONDS
            
            await client.setex(
                key,
                ttl,
                json.dumps(cached_data, default=str)
            )
            
            logger.debug(
                "Cached menu data",
                restaurant_id=restaurant_id,
                ttl=ttl,
            )
            
            return True
            
        except Exception as e:
            logger.error(
                "Error caching menu",
                restaurant_id=restaurant_id,
                error=str(e),
            )
            return False
    
    async def get_custom_data(self, cache_key: str) -> Optional[dict]:
        """Get cached custom data."""
        try:
            client = await self._get_client()
            key = self._make_key("custom", cache_key)
            
            cached_data = await client.get(key)
            if cached_data:
                logger.debug("Cache hit for custom data", cache_key=cache_key)
                return json.loads(cached_data)
            
            logger.debug("Cache miss for custom data", cache_key=cache_key)
            return None
            
        except Exception as e:
            logger.error("Error getting cached custom data", cache_key=cache_key, error=str(e))
            return None
    
    async def set_custom_data(
        self,
        cache_key: str,
        data: dict,
        ttl: Optional[int] = None
    ) -> bool:
        """Cache custom data."""
        try:
            client = await self._get_client()
            key = self._make_key("custom", cache_key)
            
            # Add timestamp to cached data
            cached_data = {
                "data": data,
                "cached_at": datetime.utcnow().isoformat(),
            }
            
            ttl = ttl or settings.CACHE_TTL_SECONDS
            
            await client.setex(
                key,
                ttl,
                json.dumps(cached_data, default=str)
            )
            
            logger.debug(
                "Cached custom data",
                cache_key=cache_key,
                ttl=ttl,
            )
            
            return True
            
        except Exception as e:
            logger.error(
                "Error caching custom data",
                cache_key=cache_key,
                error=str(e),
            )
            return False
    
    async def invalidate_menu(self, restaurant_id: str) -> bool:
        """Invalidate cached menu."""
        try:
            client = await self._get_client()
            key = self._make_key("menu", restaurant_id)
            
            result = await client.delete(key)
            
            logger.debug(
                "Invalidated menu cache",
                restaurant_id=restaurant_id,
                deleted=bool(result),
            )
            
            return bool(result)
            
        except Exception as e:
            logger.error(
                "Error invalidating menu cache",
                restaurant_id=restaurant_id,
                error=str(e),
            )
            return False
    
    async def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        try:
            client = await self._get_client()
            
            # Get all integration keys
            keys = await client.keys("integration:*")
            
            stats = {
                "total_keys": len(keys),
                "menu_keys": len([k for k in keys if b"menu:" in k]),
                "custom_keys": len([k for k in keys if b"custom:" in k]),
            }
            
            return stats
            
        except Exception as e:
            logger.error("Error getting cache stats", error=str(e))
            return {"error": str(e)}


# Create cache instance
integration_cache = IntegrationCache()