import re
from turtle import update
from typing import List
from fastapi import APIRouter, HTTPException, status, Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends
from db import db_user
from db.database import get_db
from db.models import DBUser
from schemas import UserBase, UserDisplay

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", response_model=UserDisplay, status_code=status.HTTP_201_CREATED)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)

@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    db_users = db_user.get_all_users(db)
    return db_users

@router.get("/{id}", response_model=UserDisplay)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    if id < 1:
        raise HTTPException(status_code=400, detail="Invalid ID")

    # Get the maximum user ID from the database
    max_id = db.query(func.max(DBUser.id)).scalar()
  
    if max_id is None:
        raise HTTPException(status_code=404, detail="No users found in the database")

    if id > max_id:
        raise HTTPException(status_code=400, detail=f"ID {id} is greater than the maximum user ID {max_id}")

    user = db_user.get_user_by_id(db, id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.put("/{id}/update")
def update_user(id: int,  request: UserBase, db: Session = Depends(get_db)):
    updated_user = db_user.update_user(db, id, request)
    if not updated_user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    validated_user = UserDisplay.model_validate(updated_user)
    return {
        "message": f"User {id} was updated successfully"
    }

@router.delete("/{id}/delete")
def delete_user(id: int, db: Session = Depends(get_db)):
    deleted_user = db_user.delete_user(db, id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return deleted_user