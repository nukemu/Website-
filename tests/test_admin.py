import pytest
import pytest_asyncio
import asyncio

from httpx import AsyncClient, ASGITransport

from backend.main import app


# @pytest.mark.asyncio
# async def test_set_admin():
#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url="http://test",
#         follow_redirects=True
#     ) as client:
        
#         login_payload = {
#             "username": "testuser",
#             "password": "testpass"
#         }
        
#         payload = {
#             "set_admin": {
#             "username": "testuser"
#             },
#             "verify_admin": {
#                 "username": "admin",
#                 "password": "admin"
#             }
#         }
        
#         login_response = await client.post("/auth/login", json=login_payload)
#         assert login_response.status_code == 200
        
#         access_token = login_response.cookies.get("access_token_cookie")
            
#         if not access_token:
#             set_cookie = login_response.headers.get('set-cookie', '')
#             if 'access_token_cookie' in set_cookie:
#                 access_token = set_cookie.split('access_token_cookie=')[1].split(';')[0]
                
#         client.cookies.set("access_token_cookie", access_token)
                
#         response = await client.post("/admins/set_new_admin/", json=payload)
#         assert response.status_code == 200
#         assert response.json() == {"message": 'This user alredy admin'}
        
#         await client.aclose()