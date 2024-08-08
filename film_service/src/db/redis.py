from typing import Any

from redis.asyncio import Redis
from src.core.cache import AsyncCache
import json

redis: Redis | None = None

# Функция понадобится при внедрении зависимостей


async def get_redis() -> 'AsyncRedisCache':
    return AsyncRedisCache(redis)


class AsyncRedisCache(AsyncCache):
    def __init__(self, redis_cache: Redis):
        super().__init__(redis_cache)  # Call the base class constructor

    async def get(self, key: str) -> Any | None:
        res = await self._cache.get(key)
        if not res:
            return None
        if isinstance(json.loads(res), list):
            return [json.loads(it) for it in json.loads(res)]
        return json.loads(res)

    async def set(self, key: str, value: Any, expire: int | None, **kwargs) -> None:
        await self._cache.set(key, json.dumps(value), ex=expire, **kwargs)
