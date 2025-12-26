from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with username {form_data.username} not found")
    if not utils.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

