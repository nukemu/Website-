from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "heartsc871@gmail.com"
    SMTP_PASSWORD: str = "sefv iglq byvn lysu"
    EMAIL_FROM: EmailStr = "heartsc871@gmail.com"
    
    class Config:
        env_file = ".env"
        
settings = Settings()