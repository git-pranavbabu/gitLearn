from fastapi import HTTPException, status, Depends, APIRouter
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter(
    tags=["Posts"],
    prefix="/posts"
)


#@router.get("/", response_model=List[schemas.ResponsePost])
#def read_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
@router.get("/", response_model=List[schemas.ResponsePostWithVotes]) 
def read_posts(db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
#    cursor.execute("SELECT * FROM posts")
#    posts = cursor.fetchall()
#    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    posts = ( db.query( models.Post, func.count(models.Vote.post_id).label("votes") ) .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True) .group_by(models.Post.id) .order_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit) .offset(skip) .all() )
    result = [] 
    for post, votes in posts: 
        post.votes_count = votes 
        result.append(post)
    return result




@router.get("/{id}", response_model=schemas.ResponsePost)
def read_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
#    post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#    cursor.execute("INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING *", (post.title, post.content, post.published, post.rating))
#    new_post = cursor.fetchone()
#    conn.commit()
#    print(current_user.email)
    new_post = models.Post(**post.dict())
    new_post.user_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
#    deleted_post = cursor.fetchone()
#    conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post_check = deleted_post.first()
    if not post_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post_check.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    
    return 1    

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ResponsePost)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
#    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, post.rating, id))
#    updated_post = cursor.fetchone()
#    conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    post_check = updated_post.first()

    if not post_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post_check.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    updated_post.update(post.dict(), synchronize_session=False) 
    db.commit()
    return updated_post.first()