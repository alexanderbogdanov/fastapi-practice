from fastapi import APIRouter, status, Response
from sqlalchemy.orm import Session
from fastapi import Depends
from db import db_user
from db.database import get_db
from schemas import UserBase, UserDisplay

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", response_model=UserDisplay, status_code=status.HTTP_201_CREATED)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)