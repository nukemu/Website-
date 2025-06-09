from datetime import datetime
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import EmailStr

from database import Base


class UsersOrm(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    ban_reason: Mapped[str | None] = mapped_column(String, nullable=True)
    banned_untill: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    

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
    