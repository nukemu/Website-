from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import EmailStr

from database import Base
from enum import Enum as PyEnum



class UsersOrm(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String(255))
    email_password: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    ban_reason: Mapped[str | None] = mapped_column(String, nullable=True)
    banned_untill: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    

class ServiceType(PyEnum):
    FRONTEND = "frontend"
    BACKEND = "backend"


class ServiceOrm(Base):
    __tablename__ = "services"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    service_type: Mapped[ServiceType] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    

class ResetTokenOrm(Base):
    __tablename__ = "reset_token"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used: Mapped[bool] = mapped_column(nullable=False, default=False)
    

# class BansUsersOrm(Base):
#     __tablename__ = "bans"
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     reason: Mapped[str]
#     banned_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
#     banned_untill: Mapped[datetime] = mapped_column(nullable=True)
    
#     user: Mapped["UsersOrm"] = relationship(back_populates="bans")


class DeleteAdminsOrm(Base):
    __tablename__ = "delete_admins"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String)
    reason: Mapped[str] = mapped_column(String)

