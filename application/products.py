from pydantic import BaseModel, Field, field_validator
from typing import Optional
from application.products_category import Category_Enum

class Product(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    category: Category_Enum
    price: int = Field(ge=0)
    stock: int = Field(ge=0)
    seller_id: str