from logging import config
from backend.main import app

from httpx import AsyncClient, ASGITransport

import pytest
import pytest_asyncio
import asyncio


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test") as client:
        
        yield client
        
        await client.aclose()


@pytest_asyncio.fixture
async def admin_client(client):
    login_data = {"username": "admin", "password": "admin"}
    response = await client.post("/login/", json=login_data)
    assert response.status_code == 200
    
    yield client
        
    await client.aclose()


@pytest_asyncio.fixture(autouse=True)
async def delay_between_tests():
    yield
    await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_login(client):
    response = await client.post("/login/", json={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    
    set_cookie_headers = response.headers.get("set-cookie")
    assert set_cookie_headers is not None
    assert "access_token_cookie" in set_cookie_headers
    

@pytest.mark.asyncio
async def test_logout(client):
    response = await client.post("/logout/")
    assert response.status_code == 200
    
    set_cookie_headers = response.headers.get("set-cookie")
    assert set_cookie_headers is not None
    assert 'access_token_cookie=""' in set_cookie_headers
    assert "Max-Age=0" in set_cookie_headers or "expires=" in set_cookie_headers.lower()
    print(set_cookie_headers)


@pytest.mark.asyncio
async def test_set_admin(admin_client):
    payload = {
        "username": "string",
        "verify_admin": {
            "username": "admin",
            "password": "admin"
        }
    }
    
    response = await admin_client.post("/set_new_admin/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": f"User {payload["username"]} is now an admin!"}