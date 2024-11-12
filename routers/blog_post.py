from typing import Optional

from fastapi import APIRouter, status, Response, Query
from pydantic import BaseModel

router = APIRouter(prefix="/blog", tags=["blog"])

class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool] = None



@router.post("/new/{id}", status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {"message": "Blog created",
            "data": blog.model_dump(),
            "id": id,
            "version": version}

@router.post("/new/{id}/comment}", tags=["comment"])
def create_comment(blog: BlogModel,
                   id: int,
                   comment_id: int = Query(None,
                       title="Id of the comment",
                       description="Some description for comment_id",
                       alias="commentId",
                       deprecated=True)):
    return {
        "blog": blog,
        "id": id,
        "comment_id": comment_id
    }