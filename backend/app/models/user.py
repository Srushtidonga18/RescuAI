import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLEnum
from RescuAI.backend.app.core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    RESPONDER = "RESPONDER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(SQLEnum(UserRole), default=UserRole.RESPONDER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
