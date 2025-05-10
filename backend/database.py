from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings


engine = create_async_engine(
    settings.DATA_BASE_URL_asyncpg,
    echo=True
)

session_factory = async_sessionmaker(engine)

class Base(DeclarativeBase):
    ...