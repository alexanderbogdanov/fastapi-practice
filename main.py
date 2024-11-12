from fastapi import FastAPI, status, Response
from routers.blog_get import router as blog_get_router

app = FastAPI()
app.include_router(blog_get_router)

@app.get("/hello")
def index():
    return {"message": "Hello, World!"}

