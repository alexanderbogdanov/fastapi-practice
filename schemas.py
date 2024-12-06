from typing import List, Optional
from pydantic import BaseModel, EmailStr

# Article inside the UserDisplay class is a list of Article objects 
class Article(BaseModel):
    title: str
    content: str
    published: bool
    class Config():
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class UserDisplay(BaseModel):
    username: str
    email: EmailStr
    items: List[Article] = [] 
    class Config():
        # orm_mode = True
        from_attributes = True 
        
class DeleteResponse(BaseModel):
    message: str
    
class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int
    
# User inside the ArticleDisplay class is a User object
class User(BaseModel):
    id: int
    username: str
    class Config():
        from_attributes = True
    
class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: Optional[User]
    class Config():
        from_attributes = True
        
