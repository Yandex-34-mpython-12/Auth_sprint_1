from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base_cache import AsyncCache
from src.db.postgres import db_helper
from src.db.redis import AsyncRedisCache, get_redis


class UserService:
    def __init__(self, cache: AsyncCache, db: AsyncSession):
        self.cache = cache
        self.db = db


@lru_cache()
def get_user_service(
    redis: AsyncRedisCache = Depends(get_redis),
    db: AsyncSession = Depends(db_helper.session_getter),
) -> UserService:
    return UserService(redis, db)
