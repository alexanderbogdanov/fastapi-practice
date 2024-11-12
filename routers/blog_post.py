from typing import Optional, List, Dict

from fastapi import APIRouter, status, Response, Query, Body, Path
from pydantic import BaseModel, HttpUrl

router = APIRouter(prefix="/blog", tags=["blog"])

class Image(BaseModel):
    url: HttpUrl
    alias: str


class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool] = None
    tags: List[str] = []
    metadata: Dict[str, str] = {"key_1": "value_1"}
    image: Optional[Image] = None


@router.post("/new/{id}", status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {"message": "Blog created",
            "data": blog.model_dump(),
            "id": id,
            "version": version}


@router.post("/new/{id}/comment/{comment_id}", tags=["comment"])
def create_comment(blog: BlogModel,
                   id: int,
                   comment_title: str = Query(None,
                                           title="Title of the comment",
                                           description="Some interesting description for commment_title",
                                           alias="commentTitle",
                                           deprecated=True),
                   content: str = Body(..., min_length=10, regex="^[a-z\s]*$"),
                   v: Optional[List[str]] = Query(['1.0', '1.2', '1.2'], alias="version"),
                   comment_id: int = Path(..., title="The ID of the comment", ge=5, le=10)):
    return {
        "blog": blog,
        "id": id,
        "comment_title": comment_title,
        "content": content,
        "version": v,
        'comment_id': comment_id
    }
