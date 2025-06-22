from logging import config
from backend.main import app
from backend.orm import create_tables
from backend.database import engine

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


import pytest
import pytest_asyncio
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    # Создаем таблицы перед тестом
    async with engine.begin() as conn:
        await conn.run_sync(create_tables)
    
    # Создаем сессию для теста
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
        
        # Откатываем изменения после теста
        await session.rollback()
    
    # Очищаем базу данных после теста
    async with engine.begin() as conn:
        await conn.run_sync(lambda conn: conn.execute("TRUNCATE TABLE users, other_tables CASCADE"))
    
    # Закрываем соединение с базой
    await engine.dispose()



@pytest.mark.asyncio
async def test_login(async_client, db_session):
    try:
        payload = {
            "username": "testuser",
            "password": "testpass"
        }
        
        response = await async_client.post("/auth/login/", json=payload)
        assert response.status_code == 200
    finally:
        # Явное закрытие клиента
        await async_client.aclose()