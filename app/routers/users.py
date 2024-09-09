from typing import Annotated
from datetime import datetime

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.orm import crud, schemas
from app.dependencies import get_db, get_current_user

router = APIRouter()

current_user = Annotated[schemas.User, Depends(get_current_user)]

@router.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.created_date = datetime.now()
    return crud.create_user(db=db, user=user)

@router.get("/user/", response_model=schemas.User)
def read_user(current_user:current_user, 
              db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/", response_model=list[schemas.User])
def read_users(current_user:current_user,
               skip: int = 0, 
               limit: int = 100, 
               db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/user_test/")
def read_user2():
    return {"test_request": "OK"}
  