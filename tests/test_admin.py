import pytest
import pytest_asyncio
import asyncio

from httpx import AsyncClient, ASGITransport

from backend.main import app


@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True
        ) as client:
            login_data = {"username": "admin", "password": "admin"}
            response = await client.post("/auth/login/", json=login_data)
            assert response.status_code == 200
            
            cookies = response.cookies
            access_token = cookies.get("access_token_cookie")
            
            if not access_token:
                set_cookie = response.headers.get('set-cookie', '')
                if 'access_token_cookie' in set_cookie:
                    access_token = next(
                        part.split('=')[1] for part in set_cookie.split('; ') 
                        if part.startswith('access_token_cookie=')
                    )
                else:
                    pytest.fail("Access token cookie not found")
                    
            client.cookies.update({"access_token_cookie": access_token})
            yield client
        
            await client.aclose()


@pytest.mark.asyncio
async def test_set_admin(client):
    payload = {
        "set_admin": {
        "username": "string"
        },
        "verify_admin": {
            "username": "admin",
            "password": "admin"
        }
    }
    
    response = await client.post("/admins/set_new_admin/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": 'This user alredy admin'}