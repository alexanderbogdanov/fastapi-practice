from re import A
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from db import db_article
from db.database import get_db
from schemas import ArticleBase, ArticleDisplay
from sqlalchemy.orm import Session


router = APIRouter(prefix="/article", tags=["article"])

@router.post("/", response_model=ArticleDisplay, status_code=status.HTTP_201_CREATED)
def create_article(request: ArticleBase, db: Session = Depends(get_db)):
    try:
        return db_article.create_article(db, request)
    except ValueError as e:  # Catch the duplicate error
        raise HTTPException(status_code=400, detail=str(e))
   

@router.get("/", response_model=List[ArticleDisplay])
def get_all_articles(db: Session = Depends(get_db)):
    articles = db_article.get_all_articles(db)
    return articles

@router.get("/{id}", response_model=ArticleDisplay)
def get_article_by_id(id: int, db: Session = Depends(get_db)):
    if id < 1:
        raise HTTPException(status_code=400, detail="Invalid ID")

    article = db_article.get_article_by_id(db, id)

    if article is None:
        raise HTTPException(status_code=404, detail=f"Article with id {id} not found")

    return article

@router.put("/{id}", response_model=ArticleDisplay)
def update_article(id: int, request: ArticleBase, db: Session = Depends(get_db)):
    try:
        updated_article = db_article.update_article(db, id, request)
        return updated_article
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/{id}", response_model=dict)
def delete_article(id: int, db: Session = Depends(get_db)):
    try:
        return db_article.delete_article(db, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))