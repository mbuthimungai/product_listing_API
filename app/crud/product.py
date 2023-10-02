from typing import Any, Coroutine, Dict, Optional
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession
from .base import CRUDBase
from app.schemas.product import ProductUpdate, ProductCreate
from app.models.product import Product

class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    
    async def get(self, db: AsyncSession, obj_id: str) -> Product:
        return await super().get(db, obj_id)
    
    async def get_or_create(self, db: AsyncSession, defaults: Dict[str, Any] | None, **kwargs: Any) ->  Product:
        return await super().get_or_create(db, defaults, **kwargs)
    
    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 20) -> Page[Product]:
        print(f"limit {limit}")
        return await super().get_multi(db, skip=skip, limit=limit)
    
    async def update(self, db: AsyncSession, *, obj_current: Product, obj_new: ProductUpdate | Dict[str, Any] | Product):
        return await super().update(db, obj_current=obj_current, obj_new=obj_new)
    
    async def remove(self, db: AsyncSession, *, obj_id: str) -> Product | None:
        return await super().remove(db, obj_id=obj_id)
    
product = CRUDProduct(Product)
