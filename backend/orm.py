import logging

from passlib.context import CryptContext
from sqlalchemy import select, and_
from fastapi import HTTPException, Response, status, Depends, Request

from models import UsersOrm
from database import Base, session_factory
from jwt_config import security, config


logging.basicConfig(level=logging.DEBUG)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_tables(engine):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def protected_access_token(request: Request):
    if "access_token" not in request.cookies:
        return False
    
    return True


def get_hashed_password(password: str):
    return pwd_context.hash(password)    
    

def verify_password(plain_password: str,  hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
    
    
async def register_user(username: str, password: str, response: Response):
    async with session_factory() as session:
        result = await session.execute(select(UsersOrm.username).where(UsersOrm.username==username))
        user_username = result.scalar_one_or_none()
        
        if user_username is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
        )
            
        user = UsersOrm(
            username=username, 
            hashed_password=get_hashed_password(password),
            is_admin=False,
        )
        
        session.add(user)
        await session.flush()
        token = security.create_access_token(uid=str(user.id))
        await session.commit()
        
        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=token,
            httponly=True,
            secure=False,
            max_age=3600,
            samesite="lax"
        )
        return {"message": "User registered successfully"}


async def login_user(username: str, password: str, response: Response):
    async with session_factory() as session:
        result = await session.execute(
            select(UsersOrm).where(UsersOrm.username==username))
        user = result.scalar_one_or_none()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
            
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
            
        token = security.create_access_token(uid=str(user.id))
        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=token,
            httponly=True,
            secure=False,
            max_age=config.JWT_ACCESS_TOKEN_EXPIRES,
            samesite="lax"
        )
        
        logging.debug(f"Setting cookie: {config.JWT_ACCESS_COOKIE_NAME}={token}")
        return {"message": "Login successful"}
    
    
async def check_admin(username: str, password: str):
    async with session_factory() as session:
        result = await session.execute(
            select(UsersOrm).where(
                and_(
                    UsersOrm.username==username, 
                    UsersOrm.is_admin==True
                    )
                )
            )
        
        
        user = result.scalar_one_or_none()
        
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
        ) 
        
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    return True 


async def new_admin_set(username: str):
    async with session_factory() as session:
        result = await session.execute(
            select(UsersOrm).where(UsersOrm.username==username))
        user = result.scalar_one_or_none()
    
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found",
            ) 
            
        user.is_admin = True
        await session.commit()
        
        return {"message": f"User {username} is now an admin!"}
        
    