from typing import Dict, List
from fastapi import APIRouter, HTTPException, status, Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends
from db import db_user
from db.database import get_db
from db.models import DBUser
from schemas import UserBase, UserDisplay, DeleteResponse

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", response_model=UserDisplay, status_code=status.HTTP_201_CREATED)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    try:
        return db_user.create_user(db, request)
    except ValueError as e:  # Catch the duplicate error
        raise HTTPException(status_code=400, detail=str(e))
   

@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    db_users = db_user.get_all_users(db)
    if not db_users:
        raise HTTPException(status_code=404, detail="No users found")
    return db_users

@router.get("/{id}", response_model=UserDisplay)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    if id < 1:
        raise HTTPException(status_code=400, detail="Invalid ID")

    user = db_user.get_user_by_id(db, id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.put("/{id}", response_model=dict)
def update_user(id: int,  request: UserBase, db: Session = Depends(get_db)) -> Dict[str, str]:
    try:
        updated_user = db_user.update_user(db, id, request)
        UserDisplay.model_validate(updated_user)
        return {"message": f"User {id} was updated successfully"}
    except ValueError as e:
        error_message = str(e)
        if "not found" in error_message.lower():
            raise HTTPException(status_code=404, detail=error_message)
        else:
            raise HTTPException(status_code=400, detail=error_message)


@router.delete("/{id}", response_model=DeleteResponse)
def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        return db_user.delete_user(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
