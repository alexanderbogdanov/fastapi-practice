from turtle import title
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base
from sqlalchemy.orm import relationship 


class DbUser(Base):
    __tablename__ = "users"    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    items = relationship("DbArticle", back_populates="user")
    
class DbArticle(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    published = Column(Boolean)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
        )
    user = relationship("DbUser", back_populates="items")