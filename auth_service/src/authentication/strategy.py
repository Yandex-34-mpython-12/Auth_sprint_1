from typing import TYPE_CHECKING

from fastapi_users import models
from fastapi_users.authentication import JWTStrategy
from fastapi_users.authentication.strategy.jwt import \
    JWTStrategyDestroyNotSupportedError
from fastapi_users.jwt import generate_jwt

if TYPE_CHECKING:
    from redis.asyncio import Redis


class JWTRedisStrategy(JWTStrategy):
    # def __init__(self, *args, redis: "Redis", key_prefix: str = "fastapi_users_token:", **kwargs): TODO:
    #     super().__init__(*args, **kwargs)
    #     self.redis = redis
    #     self.key_prefix = key_prefix

    async def write_token(self, user: models.UP) -> str:
        data = {
            "sub": str(user.id),
            "aud": self.token_audience,
            "roles": user.roles_as_json,
        }
        return generate_jwt(
            data, self.encode_key, self.lifetime_seconds, algorithm=self.algorithm
        )

    async def destroy_token(self, token: str, user: models.UP) -> None:
        # TODO: set в redis
        raise JWTStrategyDestroyNotSupportedError()
