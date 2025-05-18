from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UsersOrm(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    hashed_password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(nullable=True)