import os
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


# Load database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)

db_connection_str = DATABASE_URL or ""

async_engine = create_async_engine(
    db_connection_str, 
    echo=True, 
    future=True
)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async_session = async_sessionmaker(
        bind=async_engine
    )
    async with async_session() as session:
        yield session