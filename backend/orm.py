from datetime import datetime, timedelta
import logging
from typing import List, Optional

from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import select, and_, update
from fastapi import HTTPException, Query, Response, status, Depends, Request
from asyncio import create_task, sleep

from models import UsersOrm, DeleteAdminsOrm, ServiceOrm, ResetTokenOrm
from database import Base, session_factory
from jwt_config import security, config
from schemas import ServiceResponse


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


async def admin_true(username: str):
    async with session_factory() as session:
        result = await session.execute(
            select(UsersOrm).where(
                and_(
                    UsersOrm.username==username, 
                    UsersOrm.is_admin==True
                    )
                )
            )
        
        return result.scalar_one_or_none()
    
    
async def email_true(username: str, email: EmailStr):
    async with session_factory() as session:
        result = await session.execute(
            select(UsersOrm)
            .where(
                UsersOrm.email==email,
                   UsersOrm.username==username
            )
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return False
        
        return True
    
    
async def register_user(username: str, password: str, email: str, email_password: str,response: Response):
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
            email=email,
            email_password=email_password
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
            
        if user.is_banned:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Account banned. Reason: {user.ban_reason}"
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
    user = await admin_true(username)
    
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
            
        if await admin_true(username):
            return {"message": "This user alredy admin"}
            
        user.is_admin = True
        await session.commit()
        
        return {"message": f"User {username} is now an admin!"}
    
    
async def admin_delete(username: str, reason: str):
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
            return {"message": "This user are not have the admin privilegi"}
        
        user.is_admin = False
        reason_db = DeleteAdminsOrm(username=username, reason=reason)
        
        session.add(reason_db)
        await session.commit()
            
        return {"message": f"User {username} delete from admins"}
            
        
async def user_ban(username: str, reason: str, hours: int):
    async with session_factory() as session:
        result = await session.execute(
            select(UsersOrm).where(
                and_(
                    UsersOrm.username==username,
                )
            )
        )
        
        user = result.scalar_one_or_none()
        
        if not user.username:
            return {"message": "User with this name not found"}
        
        if user.is_banned:
            return {"message": "This user is already banned"}
        
        ban_time = datetime.utcnow()
        if hours == 0:
            user.banned_untill = None
            await session.commit()
        else:
            user.banned_untill = ban_time + timedelta(hours=hours)
            await session.commit()
        
        user.is_banned=True
        user.ban_reason=reason
        await session.commit()
        
        if hours > 0:
            await schedule_unban(user.id, hours)
        
        return {"message": f"The user {username} has been banned"}
    

async def schedule_unban(user_id: int, hours: int):
    async with session_factory() as session:
        sleep(hours * 3600)

        result = await session.execute(
            select(UsersOrm)
            .where(UsersOrm.id==user_id)
        )
        
        user = result.scalar_one_or_none()
        
        if user and user.is_banned and user.banned_untill:
            await session.execute(
                update(UsersOrm)
                .where(UsersOrm.id == user_id)
                .values(
                    is_banned=False,
                    ban_reason=None,
                    banned_until=None
                )
            )
            await session.commit()


async def user_unbann(username: str):
    async with session_factory() as session:
        result = await session.execute(
            select(UsersOrm).where(
                and_(
                    UsersOrm.username==username,
                    UsersOrm.is_banned==True
                )
            )
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return {"message": "There is no banned user with such nickname"}
        
        user.is_banned = False
        user.ban_reason = None
        await session.commit()
        
        return {"message": f"The user {username} has been unbanned"}
    

async def user_delete(username: str):
    async with session_factory() as session:
        result = await session.execute(
            select(UsersOrm)
            .where(UsersOrm.username==username)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this username not found"
            )
        
        await session.delete(user)
        await session.commit()
        
        return {"message": f"User '{username}' deleted successfully"}
    
    
async def service_get(
    name: Optional[str] = None,
    service_type: Optional[str] = None,
    price: Optional[int] = None
) -> List[ServiceResponse]:
    async with session_factory() as session:
        try:
            query = select(ServiceOrm)
            filters = []
            
            if name is not None:
                filters.append(ServiceOrm.name == name)
            if service_type is not None:
                filters.append(ServiceOrm.service_type == service_type.upper())
            if price is not None:
                filters.append(ServiceOrm.price == price)
                
            if filters:
                query = query.where(and_(*filters))
            
            result = await session.execute(query)
            services = result.scalars().all()
            
            if not services:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Services not found with these filters"
                )
                
            return [ServiceResponse.model_validate(s) for s in services]
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
    

async def service_add(name: str, type: str, price: int):
    async with session_factory() as session:
        service = ServiceOrm(
            name=name,
            service_type=type, 
            price=price
        )
        
        session.add(service)
        await session.commit()
        return {"message": "Service successfully added!"}
    
    
async def reset_token_add(username: str, token: str, expires_at: str | int):
    async with session_factory() as session:
        user_result = await session.execute(
            select(UsersOrm)
            .where(UsersOrm.username==username)
        )
        user = user_result.scalar_one_or_none()
        
        if not user:
            return False
            
        reset_token = ResetTokenOrm(
            token=token,
            user_id=user.id,
            expires_at=expires_at
        )
        
        session.add(reset_token)
        await session.commit()
        return True
    

async def password_reset(user_id: str, new_password: str):
    async with session_factory() as session:
        hashed_password = get_hashed_password(new_password)
        
        await session.execute(
            update(UsersOrm)
            .where(UsersOrm.id==user_id)
            .values(
                hashed_password=hashed_password
            )
        )
        await session.commit()
        return {"message": "Password successfully changed!`"}