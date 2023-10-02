# Import necessary modules and components
from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate
from app.schemas.product import Product, ProductCreate, ProductPatch, ProductUpdate
from app.api.deps import get_db
from app import crud

# Create an APIRouter instance
router = APIRouter()

# Define a route to create a new product
@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_in: ProductCreate
):
    # Use the CRUD (Create, Read, Update, Delete) operations from the 'crud' module
    # to create a new product or return an existing one if it already exists
    product, created = await crud.product.get_or_create(
        db=db, defaults=product_in.dict()
    )
    
    # If the product already exists, raise an HTTPException with a 400 status code
    if not created:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product exists"
        )
    
    # Return the created or existing product
    return product

# Define a route to retrieve a product by its ID
@router.get("/{productId}", response_model=Product, status_code=status.HTTP_200_OK)
async def get_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    productId: str
):
    # Use the CRUD operation to retrieve a product by its ID
    product = await crud.product.get(db=db, obj_id=productId)
    
    # If the product does not exist, raise an HTTPException with a 404 status code
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Return the retrieved product
    return product

# Define a route to retrieve a paginated list of products
@router.get("/", response_model=Page[Product], status_code=status.HTTP_200_OK)
async def get_products(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 20
):
    # Use the CRUD operation to retrieve multiple products with pagination
    products = await crud.product.get_multi(db=db, skip=skip, limit=limit)
    print(paginate(products))
    # If no products are found, raise an HTTPException with a 404 status code
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Products not found"
        )
    
    # Return a paginated list of products
    return paginate(products)

# Define a route to partially update a product
@router.patch("/{productId}", status_code=status.HTTP_200_OK)
async def patch_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_Id: str,
    product_in: ProductPatch
):
    # Use the CRUD operation to retrieve a product by its ID
    product = await crud.product.get(db=db, obj_id=product_Id)
    
    # If the product does not exist, raise an HTTPException with a 404 status code
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Use the CRUD operation to patch (partially update) the product
    product_patched = await crud.product.patch(db=db, obj_id=product_Id, obj_in=product_in.dict())
    
    # Return the patched product
    return product_patched

# Define a route to fully update a product
@router.put("/{productId}", response_model=Product, status_code=status.HTTP_200_OK)
async def update_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    productId: str,
    product_in: ProductUpdate
):
    # Use the CRUD operation to retrieve a product by its ID
    product = await crud.product.get(db=db, obj_id=productId)
    
    # If the product does not exist, raise an HTTPException with a 404 status code
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Use the CRUD operation to fully update the product
    product_updated = await crud.product.update(
        db=db, obj_current=product, obj_new=product_in
    )
    
    # Return the updated product
    return product_updated

# Define a route to delete a product
@router.delete("/{productId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    productId: str
):
    # Use the CRUD operation to retrieve a product by its ID
    product = await crud.product.get(db=db, obj_id=productId)
    
    # If the product does not exist, raise an HTTPException with a 404 status code
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Use the CRUD operation to remove (delete) the product
    await crud.product.remove(db=db, obj_id=productId)
    
    # Return a 204 No Content response indicating successful deletion
    return
