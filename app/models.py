from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(100), nullable=True)

class Animation(Base):
    __tablename__ = "animations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    s3_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)