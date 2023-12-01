# app/routers/friends.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.models.friend import Friend as FriendModel
from app.models.user import User

router = APIRouter()

@router.post("/users/{user_id}/add_friend/", response_model=FriendModel)
def add_friend(user_id: int, friend: FriendModel, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    friend_user = db.query(User).filter(User.id == friend.friend_id).first()
    if not friend_user:
        raise HTTPException(status_code=404, detail="Friend user not found")

    db_friend = FriendModel(**friend.dict(), user=user, friend=friend_user)
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)

    return db_friend

@router.get("/users/{user_id}/friends/", response_model=List[FriendModel])
def list_friends(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.friends

@router.get("/friends/{friend_id}", response_model=FriendModel)
def get_friend(friend_id: int, db: Session = Depends(get_db)):
    friend = db.query(FriendModel).filter(FriendModel.id == friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    return friend

@router.delete("/friends/{friend_id}", response_model=FriendModel)
def delete_friend(friend_id: int, db: Session = Depends(get_db)):
    friend = db.query(FriendModel).filter(FriendModel.id == friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    db.delete(friend)
    db.commit()

    return friend
