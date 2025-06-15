from typing import Optional
from pydantic import BaseModel, EmailStr


class UsersLoginSchema(BaseModel):
    username: str
    password: str
    
    
class UsersRegisterSchema(BaseModel):
    username: str
    password: str
    email: EmailStr
    

class SetAdmin(BaseModel):
    username: str
  
    
class CheckAdmin(BaseModel):
    username: str
    password: str
    
    
class DeleteAdmin(BaseModel):
    username: str
    reason: str
    

class BanUser(BaseModel):
    username: str
    reason: str
    hours: int
    

class UnbannUsers(BaseModel):
    username: str
    

class DeleteUsers(BaseModel):
    username: str
    

class ServiceFilter(BaseModel):
    name: str
    service_type: str
    price: int
    

class ServiceResponse(BaseModel):
    id: int
    service_type: str
    name: str
    price: int

    class Config:
        from_attributes = True 
        

class ServiceAdd(BaseModel):
    name: str
    service_type: str
    price: int