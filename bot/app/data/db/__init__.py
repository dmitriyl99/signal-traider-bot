from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import config

engine = create_async_engine(config.DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
)
