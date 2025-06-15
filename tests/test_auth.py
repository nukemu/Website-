from logging import config
from backend.main import app

from httpx import AsyncClient, ASGITransport

import pytest
import pytest_asyncio
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True
    ) as client:
        yield client
        

@pytest_asyncio.fixture(scope="function")
async def authenticated_client(client):
    login_data = {"username": "admin", "password": "admin"}
    response = await client.post("/auth/login/", json=login_data)
    
    assert response.status_code == 200, "Login failed"
    assert "access_token_cookie" in response.cookies, "Token cookie not found"
    
    yield client
    
    await client.post("/auth/logout/")


@pytest.mark.asyncio
async def test_login(client):
    response = await client.post("/auth/login/", json={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    
    set_cookie_headers = response.headers.get("set-cookie")
    assert set_cookie_headers is not None
    assert "access_token_cookie" in set_cookie_headers
    

@pytest.mark.asyncio
async def test_logout(authenticated_client):
    check_response = await authenticated_client.get("/auth/check_login/")
    assert check_response.status_code == 200
    
    response = await authenticated_client.post("/auth/logout/")
    assert response.status_code == 200
    
    set_cookie_headers = response.headers.get("set-cookie")
    assert set_cookie_headers is not None
    assert 'access_token_cookie=""' in set_cookie_headers
    assert "Max-Age=0" in set_cookie_headers or "expires=" in set_cookie_headers.lower()
    print(set_cookie_headers)
