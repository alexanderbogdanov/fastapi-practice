from enum import Enum
from typing import Optional

from fastapi import APIRouter, status, Response, Depends

from routers.blog_post import required_functionality

router = APIRouter(prefix="/blog", tags=["blog"])

@router.get("/all",
         summary='Retrieve all blogs',
         description='Retrieve all blogs from the database',
         response_description='List of blogs')
def get_all_blogs(page: int = 1, page_size: Optional[int] = 10,
                  req_parameter: dict = Depends(required_functionality)):
    return {"message": "All blogs",
            "page": page,
            "page_size": page_size,
            "req_parameter": req_parameter}


@router.get("/{id}/comments/{comment_id}", tags=["comment"])
def get_comment(id: int, comment_id: int, valid: bool = True, username: str = None,
                  req_parameter: dict = Depends(required_functionality)):
    """
    Simulates retrieving a comment from a blog
    - **id**: The blog id, mandatory path parameter
    - **comment_id**: The comment id, mandatory path parameter
    - **valid**: A boolean, optional query parameter
    - **username**: A string, optional query parameter
    """
    return {"message": f"Comment with id {comment_id} from blog with id {id}",
            "valid": valid,
            "username": username,
            "req_parameter": req_parameter}



class BlogType(str, Enum):
    short = "short"
    story = "story"
    howto =  "howto"

@router.get("/type/{type}")
def get_blog_type(type: BlogType):
    return {"message": f"Blogs of type {type}"}

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_blog(id: int, response: Response):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Blog with id {id} not found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": f"Blog with id {id}"}