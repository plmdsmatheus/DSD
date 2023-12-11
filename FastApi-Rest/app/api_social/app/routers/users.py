from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.models.user import User as UserModel
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like

router = APIRouter()

@router.post("/users/", response_model=UserModel)
def create_user(user: UserModel, db: Session = Depends(get_db)):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.get("/users/", response_model=List[UserModel])
def list_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()

@router.get("/users/{user_id}", response_model=UserModel)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user