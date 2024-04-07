from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    price: int
    stock: int = Field(ge=0)
    seller_id: str