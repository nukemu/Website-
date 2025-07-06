from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select

from models import ResetTokenOrm
from orm import login_user, register_user, email_true, reset_token_add, password_reset
from schemas import UsersLoginSchema, UsersRegisterSchema, PasswordReset, CheckEmail, ResetPassword
from jwt_config import security, config
from routers.email_utils import send_password_reset_email
from database import session_factory

import secrets


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
    return await register_user(cred.username, cred.password, cred.email, cred.email_password, response)

    
@router.post("/logout/")
async def logout(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "Successfully logged out"}    


@router.post("/forgot_password/")
async def forgot_password(request: PasswordReset, check_email: CheckEmail):
    if not await email_true(check_email.username, check_email.email):
        return {"message": "Incorrect username or email"}

    reset_token = secrets.token_urlsafe(32)
    expires = datetime.now() + timedelta(hours=1)
    
    if not await reset_token_add(check_email.username, reset_token, expires):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {check_email.username} not found"
        )
        
    await send_password_reset_email(request.email, reset_token)
    
    return {"message": "Если email зарегистрирован, на него отправлена инструкция"} 


@router.post("/reset_password/")
async def reset_password(form: ResetPassword):
    async with session_factory() as session:
        token_response = await session.execute(
            select(ResetTokenOrm)
            .where(ResetTokenOrm.token==form.token)
        )
        tokens = token_response.scalar_one_or_none()
        
        if not tokens:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect reset token"
            )
        
        if datetime.now() > tokens.expires_at:
                raise HTTPException(status_code=400, detail="Срок действия токена истек")
        
        user_id = tokens.user_id
        tokens.used = True
        await session.commit()
        
        return await password_reset(user_id, form.new_password)
    

@router.get("/check_login/", dependencies=[Depends(security.access_token_required)])
async def check_login():
    return {"message": "You have the access token!"}