from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str      # Name of the product (required)
    price: str     # Price of the product (required)
    image: str     # URL or path to the product image (required)
    weight: str    # Weight of the product (required)
    
class ProductCreate(ProductBase):
    ...
    
class ProductUpdate(ProductBase):
    ...
    
class ProductPatch(ProductBase):
    name: Optional[str]   # Name is optional for patching
    price: Optional[str]  # Price is optional for patching
    image: Optional[str]  # Image is optional for patching
    weight: Optional[str] # Weight is optional for patching


class Product(ProductBase):
    id: str
        
    class Config:
        orm_mode = True