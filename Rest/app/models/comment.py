from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.models.base import Base  # Importe diretamente a classe Base

class CommentBase(BaseModel):
    user_id: int
    post_id: int
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True
