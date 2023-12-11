from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.models.post import Post as PostModel
from app.models.user import User
from app.models.comment import Comment
from app.models.like import Like

router = APIRouter()

@router.post("/users/{user_id}/posts/", response_model=PostModel)
def create_post(user_id: int, post: PostModel, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_post = PostModel(**post.dict(), user=user)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post

@router.get("/posts/", response_model=List[PostModel])
def list_posts(db: Session = Depends(get_db)):
    return db.query(PostModel).all()

@router.get("/posts/{post_id}", response_model=PostModel)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post

@router.delete("/posts/{post_id}", response_model=PostModel)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()

    return post