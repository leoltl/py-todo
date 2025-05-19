import os
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models import Base

# Load database URL from environment
HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")

db_connection_str = f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{5432}/{DB_NAME}"

async_engine = create_async_engine(
    db_connection_str,
    echo=True,
    future=True
)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async_session = async_sessionmaker(
        bind=async_engine
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session
