from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate
from app.schemas.product import Product, ProductCreate, ProductPatch, ProductUpdate
from app.api.deps import get_db
from app import crud

router = APIRouter(
    
)

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_in: ProductCreate
    ):

    product, created = await crud.product.get_or_create(
        db=db, defaults=product_in.dict()
    )
    if not created:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product exists"
        )
    return product

@router.get("/{productId}", response_model=Product, status_code=status.HTTP_200_OK)
async def get_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    productId: str
):
    product = await crud.product.get(db=db, obj_id=productId)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.get("/", response_model=Page[Product], status_code=status.HTTP_200_OK)
async def get_products(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 20
):
    products = await crud.product.get_multi(db=db, skip=skip, limit=limit)
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Products not found"
        )
    return paginate(products)

@router.patch("/{productId}", status_code=status.HTTP_200_OK)
async def patch_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_Id: str,
    product_in: ProductPatch
):
    product = await crud.product.get(db=db, obj_id=product_Id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    product_patched = await crud.product.patch(db=db, obj_id=product_Id,
                                               obj_in=product_in.dict())
    return product_patched

@router.put("/{productId}", response_model=Product, status_code=status.HTTP_200_OK)
async def update_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    productId: str,
    product_in: ProductUpdate
):
    product = await crud.product.get(db=db, obj_id=productId)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    product_updated = await crud.product.update(
        db=db, obj_current=product, obj_new=product_in
    )
    return product_updated

@router.delete("/{productId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    productId: str
):
    product = await crud.product.get(db=db, obj_id=productId)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    await crud.product.remove(db=db, obj_id=productId)
    return