from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    price: int
    stock: int
    seller_id: str