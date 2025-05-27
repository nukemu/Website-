from logging import config
from backend.main import app

from httpx import AsyncClient, ASGITransport

import pytest
import pytest_asyncio
import asyncio



@pytest_asyncio.fixture
async def get_jwt_token():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True
    ) as client:
        response = await client.post("/login/", json={"username": "admin", "password": "admin"})
        assert response.status_code == 200
        
        set_cookie = response.headers.get("set-cookie")
        assert set_cookie is not None, "Куки отсутствуют в ответе"
        
        token = set_cookie.split("access_token_cookie=")[1]
        print("access token: ", f"{token}")
        
        return token 
    
    
@pytest_asyncio.fixture(autouse=True)
async def get_login():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True
    ) as client:
        login_response = await client.post("/login/", json={
                    "username": "admin",
                    "password": "admin"
        })


async def test_logout(get_login):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True
    ) as client:
        response = await client.post("/logout/")
        assert response.status_code == 200
        
        set_cookie = response.headers.get("set-cookie")
        assert set_cookie is not None, "Не получен заголовок Set_Cookie"
        
        assert 'access_token_cookie=""' in set_cookie
        assert "Max-Age=0" in set_cookie or "expires=" in set_cookie
        
        print(f"Куки для удаления: {set_cookie}")
        