import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from src.api.v1 import users, health
from src.core.config import settings
from src.core.logger import LOGGING
from src.db import redis, postgres


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on_startup
    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)

    await postgres.create_database()

    yield
    # on_shutdown
    await redis.redis.aclose()

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


app.include_router(users.router, prefix='/api/v1/users', tags=['users'])
app.include_router(health.router, prefix='/api/health', tags=['health'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8001,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
