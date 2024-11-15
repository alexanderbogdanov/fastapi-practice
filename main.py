from fastapi import FastAPI, status, Response
from db.models import Base
from db.database import engine
from routers.blog_get import router as blog_get_router
from routers.blog_post import router as blog_post_router

app = FastAPI()
app.include_router(blog_get_router)
app.include_router(blog_post_router)

@app.get("/hello")
def index():
    return {"message": "Hello, World!"}

Base.metadata.create_all(bind=engine)