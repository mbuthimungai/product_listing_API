# Import the APIRouter class from FastAPI
from fastapi import APIRouter

# Import the 'products' router from the 'app.api.v1.endpoints' module
from app.api.v1.endpoints import products

# Create an instance of the APIRouter
router = APIRouter()

# Include the 'products' router as a sub-router under the '/products' prefix
# and assign the tag "Products" to group related API endpoints
router.include_router(products.router, prefix="/products", tags=["Products"])
