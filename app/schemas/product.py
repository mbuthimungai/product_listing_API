from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: str
    image: str
    weight: str
    
class ProductCreate(ProductBase):
    ...
    
class ProductUpdate(ProductBase):
    ...
    
class ProductPatch(ProductBase):
    name: Optional[str]
    price: Optional[str]
    image: Optional[str]
    weight: Optional[str]


class Product(ProductBase):
    id: str
    
    
    class Config:
        orm_mode = True