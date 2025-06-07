from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings


engine = create_async_engine(
    settings.DATA_BASE_URL_asyncpg,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True
)

session_factory = async_sessionmaker(engine)

class Base(DeclarativeBase):
    ...