import logging
import os
from logging import config as logging_config

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class RunConfig(BaseModel):
    project_name: str = 'movies'
    host: str = "0.0.0.0"
    port: int = 8001
    log_level: int = logging.DEBUG
    version: str = '0.0.1'


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    oauth: str = "/oauth"
    users: str = "/users"
    roles: str = "/roles"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    @property
    def bearer_token_url(self) -> str:
        # v1/auth/login
        parts = (self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")

    @property
    def oauth2_bearer_token_url(self) -> str:
        # v1/auth/login
        parts = (self.v1.prefix, self.v1.oauth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")


class DatabaseConfig(BaseModel):
    host: str = '127.0.0.1'
    port: int = 5432
    db_name: str
    user: str
    password: str

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self) -> str:
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'


class CacheConfig(BaseModel):
    host: str
    port: int


class AccessToken(BaseModel):
    jwt_encode_secret: str
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class JaegerConfig(BaseModel):
    agent_host_name: str = 'localhost'
    agent_port: int = 6831


class OAuth2Config(BaseModel):
    yandex_url: str = 'https://oauth.yandex.ru'
    client_id: str
    client_secret: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    cache: CacheConfig
    access_token: AccessToken
    jaeger: JaegerConfig = JaegerConfig()
    oauth: OAuth2Config


settings = Settings()

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
