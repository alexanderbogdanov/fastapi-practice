import re
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
    # Check if the ID is less than 1
    if id < 1:
        raise HTTPException(status_code=400, detail="Invalid ID")

    # Get the maximum user ID from the database
    max_id = db.query(func.max(DBUser.id)).scalar()

    # Handle the case where max_id is None
    if max_id is None:
        raise HTTPException(status_code=404, detail="No users found in the database")

    # Check if the provided ID is greater than the maximum ID
    if id > max_id:
        raise HTTPException(status_code=400, detail=f"ID {id} is greater than the maximum user ID {max_id}")

    # Get the user by ID
    user = db_user.get_user_by_id(db, id)

    # Check if the user is not found
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user