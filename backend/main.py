import asyncio
import uvicorn

from fastapi import FastAPI, HTTPException, Depends, Response, Request, status
from fastapi.middleware.cors import CORSMiddleware

from schemas import UsersLoginSchema, UsersRegisterSchema, CheckAdmin, SetAdmin, DeleteAdmin
from jwt_config import security, config
from orm import register_user, login_user, create_tables, check_admin, new_admin_set, admin_delete
from database import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login/")
async def login(cred: UsersLoginSchema, response: Response):
    # response = Response()
    print("Login attempt for:", cred.username)  # Логируем попытку входа
    result = await login_user(cred.username, cred.password, response)
    print("Response cookies:", response.headers.get("set-cookie"))  # Логируем куки
    return result
    
    
@app.post("/register/")
async def register(cred: UsersRegisterSchema, response: Response):
    return await register_user(cred.username, cred.password, response)

    
@app.post("/logout/")
async def logout(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Successfully logged out"}    


@app.get("/check_login/", dependencies=[Depends(security.access_token_required)])
async def check_login():
    return {"message": "You have the access token!"}


@app.post("/set_new_admin/", dependencies=[Depends(security.access_token_required)])
async def set_new_admin(set_admin: SetAdmin, verify_admin: CheckAdmin):
    if not await check_admin(verify_admin.username, verify_admin.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have administrator privileges"
        )
    
    return await new_admin_set(set_admin.username)


@app.post("/delete_admin/", dependencies=[Depends(security.access_token_required)])
async def delete_admin(set_admin: SetAdmin, delete_admin: DeleteAdmin):
    if await check_admin(delete_admin.username, delete_admin.password):
        return await admin_delete(set_admin.username)


if __name__ == "__main__":
    asyncio.run(create_tables(engine))
    uvicorn.run("main:app", reload=True)