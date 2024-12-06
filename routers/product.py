from fastapi import APIRouter


router = APIRouter(prefix="/products", tags="products")  # This is a dummy router to simulate a product router

products = ["watch", "laptop", "phone", "tablet"]

router.get("/")
def get_products():
    return products