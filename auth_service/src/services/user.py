from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.db.base_cache import AsyncCache
from src.db.postgres import get_session
from src.db.redis import AsyncRedisCache, get_redis
from src.models.token import Token
from src.models.user import User
from src.schemas.user import UserCreate


class UserService:
    def __init__(self, cache: AsyncCache, db: AsyncSession):
        self.cache = cache
        self.db = db

    async def create_user(self, user_create: UserCreate) -> User:
        user_dto = user_create.model_dump()
        user = User(**user_dto)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_login(self, login: str) -> User | None:
        stmt = select(User).where(User.login == login)
        user = await self.db.scalar(stmt)
        return user

    async def get_user_by_id(self, user_id: str) -> User | None:
        stmt = select(User).where(User.id == user_id)
        user = await self.db.scalar(stmt)
        return user

    async def get_token_by_user_id(self, user_id: str | UUID) -> Token | None:
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        stmt = select(Token).where(Token.user_id == user_id)
        user = await self.db.scalar(stmt)
        return user

    async def authenticate_user(self, login: str, password: str) -> User | None:
        user = await self.get_user_by_login(login)
        if not user:
            return None
        if not user.check_password(password):
            return None
        return user

    async def create_token(self, user_id: str | UUID, refresh_token: str) -> Token:
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        token = Token(refresh_token=refresh_token, user_id=user_id)
        self.db.add(token)
        await self.db.commit()
        await self.db.refresh(token)
        return token

    async def create_or_update_token(self, user_id: str | UUID, refresh_token: str) -> Token:
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        token = await self.get_token_by_user_id(user_id)
        if not token:
            token = await self.create_token(user_id, refresh_token)
        else:
            token.refresh_token = refresh_token
            await self.db.commit()
            await self.db.refresh(token)
        return token

    async def check_refresh_token(self, user_id: str, refresh_token: str) -> bool:
        token = await self.get_token_by_user_id(user_id)
        if not token:
            return False

        return token.refresh_token == refresh_token

    async def invalidate_access_token(self, user_id: str, access_token: str) -> None:
        cache_key = f"{user_id}_logout"
        await self.cache.set(cache_key, access_token, settings.access_token_expires_min)


@lru_cache()
def get_user_service(
    redis: AsyncRedisCache = Depends(get_redis),
    db: AsyncSession = Depends(get_session),
) -> UserService:
    return UserService(redis, db)
