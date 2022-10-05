from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_async_engine(settings.database_url, echo=True, future=True)
sync_engine = create_engine(settings.database_url.replace('+asyncpg', ''), echo=True)

async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
)

Session = sessionmaker(sync_engine)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
