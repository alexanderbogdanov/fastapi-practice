from typing import List, Optional
from db.models import DbArticle
from sqlalchemy.orm import Session
from schemas import ArticleBase

def create_article(db: Session, request: ArticleBase) -> DbArticle:
    new_article = DbArticle(
        title = request.title, 
        content = request.content,
        published = request.published,
        user_id = request.creator_id
        )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

def get_all_articles(db: Session) -> List[DbArticle]:
    return db.query(DbArticle).all()

def get_article_by_id(db: Session, id: int) -> Optional[DbArticle]:
    return db.query(DbArticle).filter(DbArticle.id == id).first()

def update_article(db: Session, id: int, request: ArticleBase) -> DbArticle:
    article = db.query(DbArticle).filter(DbArticle.id == id).first()
    if not article:
        raise ValueError(f"Article with id {id} not found")
    article.title = request.title
    article.content = request.content
    article.published = request.published
    article.user_id = request.creator_id
    
    db.commit()
    db.refresh(article)
    return article

def delete_article(db: Session, id: int) ->dict:
    article = db.query(DbArticle).filter(DbArticle.id == id).first()
    if not article:
        raise ValueError(f"Article wit id {id} not found")
    db.delete(article)
    db.commit()
    return {"message": f"Article with id {id} was deleted successfully"}
    pass