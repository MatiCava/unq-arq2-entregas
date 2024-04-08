from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Product(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    price: int = Field(ge=0)
    stock: int = Field(ge=0)
    seller_id: str