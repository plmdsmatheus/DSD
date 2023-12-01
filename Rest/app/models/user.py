# app/models/user.py

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base  # Importe diretamente a classe Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    password = Column(String)

    # Relacionamentos
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
