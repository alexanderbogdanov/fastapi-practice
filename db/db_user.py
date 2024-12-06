from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from db.hashing import Hash
from db.models import DbUser
from schemas import UserBase

def create_user(db: Session, request: UserBase) -> DbUser:
    # Check if the username already exists
    if db.query(DbUser).filter(DbUser.username == request.username).first():
        raise ValueError("Username already exists")
    
    # Check if the email already exists
    if db.query(DbUser).filter(DbUser.email == request.email).first():
        raise ValueError("Email already exists")
    
    new_user = DbUser(
        username = request.username, 
        email = request.email, 
        password = Hash.bcrypt(request.password)
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session) -> List[DbUser]:
    return db.query(DbUser).all()
   

def get_user_by_id(db: Session, id: int) -> Optional[DbUser]:
    return db.query(DbUser).filter(DbUser.id == id).first()

def update_user(db: Session, id: int, request: UserBase) -> DbUser:
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise ValueError(f"User with id {id} not found")
    
    duplicate_user = db.query(DbUser).filter(
        (DbUser.username == request.username) | (DbUser.email == request.email),
        DbUser.id != id
    ).first()
    
    if duplicate_user:
        if duplicate_user.username == request.username:
            raise ValueError("Username already exists")
        if duplicate_user.email == request.email:
            raise ValueError("Email already exists")
        
    user.username = request.username
    user.email = request.email
    user.password = Hash.bcrypt(request.password)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, id: int) -> Dict[str, str]:
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise ValueError(f"User with id {id} not found")
    db.delete(user)
    db.commit()
    return {
        "message": f"User {id} was deleted successfully"
    }