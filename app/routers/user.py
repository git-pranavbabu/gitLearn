from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    tags=["Users"],
    prefix="/users"
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUser)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())    
    db.add(new_user)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {user.email} already exists")
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.ResponseUser)
def read_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

@router.get("/", response_model=List[schemas.ResponseUser])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    user_check = user.first()
    if not user_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return 1
