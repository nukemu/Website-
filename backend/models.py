from sqlalchemy.orm import Mapped, mapped_column
from pydantic import Field

from database import Base


class UsersOrm(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    hashed_password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(nullable=True)
    

class DeleteAdminsOrm(Base):
    __tablename__ = "delete_admins"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    reason: Mapped[str] = Field(..., min_length=10, max_length=50)
    