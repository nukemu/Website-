import asyncio
import uvicorn

from fastapi import FastAPI, HTTPException, Depends, Response, Request
from fastapi.middleware.cors import CORSMiddleware

from schemas import UsersLoginSchema, UsersRegisterSchema
from jwt_config import security, config
from orm import register_user, login_user, create_tables
from database import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login")
async def login(cred: UsersLoginSchema):
    response = Response()
    return await login_user(cred.username, cred.password, response)
    
    
@app.post("/register")
async def register(cred: UsersRegisterSchema, response: Response):
    return await register_user(cred.username, cred.password, response)

    
@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Successfully logged out"}    


@app.get("/check_login", dependencies=[Depends(security.access_token_required)])
async def check_login():
    return {"message": "You have the access token!"}




if __name__ == "__main__":
    asyncio.run(create_tables(engine))
    uvicorn.run("main:app", reload=True)