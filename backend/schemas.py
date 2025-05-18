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