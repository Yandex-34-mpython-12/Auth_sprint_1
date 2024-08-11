from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from api import router as api_router

from src.core.config import settings
from src.core.logger import LOGGING
from src.db import redis, postgres


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on_startup
    redis.redis = Redis(host=settings.cache.host, port=settings.cache.port, decode_responses=True)

    await postgres.create_database()  # TODO: DEL after alembic

    yield
    # on_shutdown
    await redis.redis.aclose()

app = FastAPI(
    title=settings.run.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        log_config=LOGGING,
        log_level=settings.run.log_level,
    )
