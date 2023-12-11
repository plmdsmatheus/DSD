from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base  # Importe diretamente a classe Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    content = Column(String)

    # Relacionamentos
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

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