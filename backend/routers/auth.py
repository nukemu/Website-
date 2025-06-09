from fastapi import APIRouter, Depends, Response

from orm import login_user, register_user
from schemas import UsersLoginSchema, UsersRegisterSchema
from jwt_config import security, config


router = APIRouter(
    prefix="/auth",
    tags=["authorisations"]
)


@router.post("/login/")
async def login(cred: UsersLoginSchema, response: Response):
    # response = Response()
    print("Login attempt for:", cred.username)
    result = await login_user(cred.username, cred.password, response)
    print("Response cookies:", response.headers.get("set-cookie"))
    return result
    
    
@router.post("/register/")
async def register(cred: UsersRegisterSchema, response: Response):
    return await register_user(cred.username, cred.password, cred.email, response)

    
@router.post("/logout/")
async def logout(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Successfully logged out"}    


@router.get("/check_login/", dependencies=[Depends(security.access_token_required)])
async def check_login():
    return {"message": "You have the access token!"}