from typing import Any, Dict, Generic, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, update
from fastapi.encoders import jsonable_encoder
from fastapi_pagination import Page

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
       Generic CRUD (Create, Read, Update, Delete) operations for SQLAlchemy models.

    This class provides a set of generic CRUD operations that can be used with SQLAlchemy models.
    It includes methods for creating, retrieving, updating, and deleting records in the database.

    Args:
        model (Type[ModelType]): The SQLAlchemy model class to perform CRUD operations on.

    Example:
        To create a CRUD instance for a specific model (e.g., User model):

        ```python
        crud_user = CRUDBase[Prodcut, ProductCreateSchema, ProductUpdateSchema]
        ```
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model
    # get single instance
    async def get(self, db: AsyncSession, obj_id: str) -> Optional[ModelType]:
        query = await db.execute(select(self.model).where(self.model.id == obj_id))
        return query.scalar_one_or_none()
    
    # get all multiple entities
    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> Page[ModelType]:
        query = await db.execute(select(self.model).offset(skip).limit(limit))
        return query.scalars().all()
    
    # search a specific entity
    async def get_by_params(self, db: AsyncSession, **params: Any) -> Optional[ModelType]:
        query = select(self.model)
        for key, value in params.items():
            if isinstance(value, str):
                query = query.where(func.lower(getattr(self.model, key)) == func.lower(value))
            else:
                query = query.where(getattr(self.model, key) == value)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    # add an entity
    async def get_or_create(self, db: AsyncSession,
                            defaults: Optional[Dict[str, Any]], **kwargs: Any) -> ModelType:
        instance = await self.get_by_params(db, **kwargs)
        if instance:
            return instance, False
        params = defaults or {}
        params.update(kwargs)
        instance = self.model(**params)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance, True
    
    # Partially update an entity
    async def patch(self, db: AsyncSession,
                    *, obj_id: str,
                    obj_in: UpdateSchemaType | Dict[str, Any]
                    ) -> Optional[ModelType]:
        db_obj = await self.get(db=db, obj_id=obj_id)
        if not db_obj:
            return None
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        query = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**update_data)
        )
        await db.execute(query)
        return await self.get(db, obj_id)
    
    # Fully update an entity
    async def update(
        self,
        db: AsyncSession,
        *,
        obj_current: ModelType,
        obj_new: UpdateSchemaType | Dict[str, Any] | ModelType
    ):
        obj_data = jsonable_encoder(obj_current)
        
        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])
        db.add(obj_current)
        await db.commit()
        await db.refresh(obj_current)
        return obj_current
    
    
    # fully delete an entity from db
    async def remove(self, db: AsyncSession, *, obj_id: str) -> Optional[ModelType]:
        db_obj = await self.get(db, obj_id)
        if not db_obj:
            return None

        await db.delete(db_obj)
        await db.commit()

        return db_obj
