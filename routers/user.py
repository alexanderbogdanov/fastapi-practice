from fastapi import APIRouter, status, Response
from sqlalchemy.orm import Session
from fastapi import Depends
from db.database import get_db
from schemas import UserBase

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    return {"message": "User created successfully"}