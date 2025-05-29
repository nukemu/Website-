from pydantic import BaseModel


class UsersLoginSchema(BaseModel):
    username: str
    password: str
    
    
class UsersRegisterSchema(BaseModel):
    username: str
    password: str
    

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
    time: int