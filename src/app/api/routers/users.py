from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import crud, schemas, connection
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(connection.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(connection.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{token}", response_model=schemas.User)
def get_user_by_token(token: str, db: Session = Depends(connection.get_db)):
    db_user = crud.get_user_by_token(db, token=token)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user