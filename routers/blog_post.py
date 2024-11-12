from fastapi import APIRouter, status, Response

router = APIRouter(prefix="/blog", tags=["blog"])

@router.post("/new")
def create_blog():
    return {"message": "Blog created"}