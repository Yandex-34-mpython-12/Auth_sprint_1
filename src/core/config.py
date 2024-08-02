import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../../.env', env_file_encoding='utf-8')
    
    project_name: str = Field('movies', alias='PROJECT_NAME')
    redis_host: str = Field('127.0.0.1', alias='REDIS_HOST')
    redis_port: int = Field(6379, alias='REDIS_PORT')

    pg_host: str = Field('127.0.0.1', alias='POSTGRES_HOST')
    pg_port: int = Field(5432, alias='POSTGRES_PORT')
    pg_db: str = Field('movies_database', alias='POSTGRES_DB')
    pg_user: str = Field('postgres', alias='POSTGRES_USER')
    pg_password: str = Field('postgres', alias='POSTGRES_PASSWORD')

    token_secret_key: str = Field('secret', alias='TOKEN_SECRET_KEY')
    access_token_expires_min: int = Field(60, alias='ACCESS_TOKEN_EXPIRES_MIN')
    refresh_token_expires_days: int = Field(10, alias='REFRESH_TOKEN_EXPIRES_DAYS')


settings = Settings()

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
