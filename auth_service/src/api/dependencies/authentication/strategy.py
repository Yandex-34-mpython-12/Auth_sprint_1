from typing import Optional

import jwt
import redis.asyncio

from fastapi_users.authentication import JWTStrategy, RedisStrategy
from fastapi_users import models, BaseUserManager, exceptions
from fastapi_users.jwt import generate_jwt, decode_jwt

from src.authentication.strategy import JWTRedisStrategy
from src.core.config import settings


def get_jwt_strategy() -> JWTRedisStrategy:
    return JWTRedisStrategy(
        secret=settings.access_token.jwt_encode_secret,
        lifetime_seconds=settings.access_token.lifetime_seconds
    )
