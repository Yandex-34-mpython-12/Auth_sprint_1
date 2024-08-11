from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base_cache import AsyncCache
from src.db.postgres import db_helper
from src.db.redis import AsyncRedisCache, get_redis
from src.schemas import PermissionCreate


class UserService:
    def __init__(self, cache: AsyncCache, db: AsyncSession):
        self.cache = cache
        self.db = db

    async def create_permission(self, permission_create: PermissionCreate) -> Permission:
        permission_dto = permission_create.model_dump()
        permission = Permission(**permission_dto)
        self.db.add(permission)
        await self.db.commit()
        await self.db.refresh(permission)
        return permission

    async def add_permission_to_user(self, user_id, permission_id) -> UserPermission:
        user_permission = UserPermission(user_id=user_id, permission_id=permission_id)
        self.db.add(user_permission)
        await self.db.commit()
        await self.db.refresh(user_permission)
        return user_permission

@lru_cache()
def get_user_service(
    redis: AsyncRedisCache = Depends(get_redis),
    db: AsyncSession = Depends(db_helper.session_getter),
) -> UserService:
    return UserService(redis, db)
