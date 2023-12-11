from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.user import User

class FriendBase(BaseModel):
    user_id: int
    friend_id: int

class FriendCreate(FriendBase):
    pass

class Friend(FriendBase):
    id: int

    class Config:
        orm_mode = True