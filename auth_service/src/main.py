from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis
from src.api import router as api_router
from src.core.config import settings
from src.core.logger import LOGGING
from src.core.tracer import configure_tracer
from src.db import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on_startup
    redis.redis = Redis(host=settings.cache.host, port=settings.cache.port, decode_responses=True)

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

# Настраимаем Jaeger
configure_tracer()
FastAPIInstrumentor.instrument_app(app)


# @app.middleware('http')
# async def before_request(request: Request, call_next):
#     response = await call_next(request)
#     request_id = request.headers.get('X-Request-Id')
#     if not request_id:
#         return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'X-Request-Id is required'})
#     return response


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        log_config=LOGGING,
        log_level=settings.run.log_level,
    )
