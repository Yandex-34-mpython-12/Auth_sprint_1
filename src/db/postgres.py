from sqlalchemy import event, text

from core.config import settings
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


class Base(DeclarativeBase):
    pass


dsn = f'postgresql+asyncpg://{settings.pg_user}:{settings.pg_password}@{settings.pg_host}:{settings.pg_port}/{settings.pg_db}'
engine = create_async_engine(dsn, echo=True, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@event.listens_for(Base.metadata, "before_create")
def create_schemas(target, connection, **kw):
    schemas = set()
    for table in target.tables.values():
        if table.schema is not None:
            schemas.add(table.schema)
    for schema in schemas:
        connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS %s" % schema)
        )
