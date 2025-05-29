from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import Field

from database import Base


class UsersOrm(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    hashed_password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(nullable=True, default=False)
    is_banned: Mapped[bool] = mapped_column(default=False)
    ban_reason: Mapped[str] = mapped_column(nullable=True)
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
    username: Mapped[str]
    reason: Mapped[str]
    