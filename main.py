from enum import Enum

from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def index():
    return {"message": "Hello, World!"}

@app.get("/blog/all")
def get_all_blogs(page: int = 1, page_size: int = 10):
    return {"message": "All blogs",
            "page": page,
            "page_size": page_size}


@app.get("/blog/{id}/comments/{comment_id}")
def get_comment(id: int, comment_id: int, valid: bool = True, username: str = None):
    return {"message": f"Comment with id {comment_id} from blog with id {id}",
            "valid": valid,
            "username": username}



class BlogType(str, Enum):
    short = "short"
    story = "story"
    howto =  "howto"

@app.get("/blog/type/{type}")
def get_blog_type(type: BlogType):
    return {"message": f"Blogs of type {type}"}

@app.get("/blog/{id}")
def get_blog(id: int):
    return {"message": f"Blog with id {id}"}