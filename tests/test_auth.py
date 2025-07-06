from logging import config
from backend.main import app
from backend.orm import create_tables
from backend.database import engine

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


import pytest
import pytest_asyncio
import asyncio


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True
    ) as client:
        
        payload = {
            "username": "testuser",
            "password": "testpass"
        }
        
        response = await client.post("/auth/login/", json=payload)
        assert response.status_code == 200
        

@pytest.mark.asyncio
async def test_logout():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True
    ) as client:
        
        payload = {
            "username": "testuser",
            "password": "testpass"
        }
        
        login_response = await client.post("/auth/login/", json=payload)
        assert login_response.status_code == 200
        
        login_cookies = login_response.headers.get("set-cookie")
        assert login_cookies is not None
        assert "access_token_cookie=" in login_cookies
                
        logout_response = await client.post("/auth/logout/")
        assert logout_response.status_code == 200
        
        logout_cookies = logout_response.headers.get("set-cookie")
        assert logout_cookies is not None
        
        # assert set_cookie_headers is not None
        # assert 'access_token_cookie=""' in set_cookie_headers
        # assert "Max-Age=0" in set_cookie_headers or "expires=" in set_cookie_headers.lower()

        # await client.aclose()
        
        
