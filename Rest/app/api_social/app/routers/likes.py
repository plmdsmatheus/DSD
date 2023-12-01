# app/routers/likes.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.models.like import Like as LikeModel
from app.models.user import User
from app.models.post import Post

router = APIRouter()

@router.post("/posts/{post_id}/like/", response_model=LikeModel)
def like_post(post_id: int, like: LikeModel, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == like.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Lógica para adicionar um like ao post
    new_like = LikeModel(**like.dict(), post=post, user=user)
    post.likes.append(new_like)
    
    # Salvando alterações no banco de dados
    db.commit()
    db.refresh(post)

    return like

@router.get("/posts/{post_id}/likes/", response_model=List[LikeModel])
def list_likes(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post.likes

@router.delete("/likes/{like_id}", response_model=LikeModel)
def unlike_post(like_id: int, db: Session = Depends(get_db)):
    like = db.query(LikeModel).filter(LikeModel.id == like_id).first()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(like)
    db.commit()

    return like
