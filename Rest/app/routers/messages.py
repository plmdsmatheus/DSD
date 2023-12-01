from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.models.comment import Comment as CommentModel
from app.models.user import User
from app.models.post import Post

router = APIRouter()

@router.post("/posts/{post_id}/comments/", response_model=CommentModel)
def create_comment(post_id: int, comment: CommentModel, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == comment.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db_comment = CommentModel(**comment.dict(), post=post, user=user)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment

@router.get("/posts/{post_id}/comments/", response_model=List[CommentModel])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post.comments

@router.get("/comments/{comment_id}", response_model=CommentModel)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment

@router.delete("/comments/{comment_id}", response_model=CommentModel)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(comment)
    db.commit()

    return comment
