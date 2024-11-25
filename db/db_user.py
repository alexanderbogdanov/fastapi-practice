from sqlalchemy.orm import Session
from db.hashing import Hash
from db.models import DBUser
from schemas import UserBase

def create_user(db: Session, request: UserBase):
    new_user = DBUser(username = request.username, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user