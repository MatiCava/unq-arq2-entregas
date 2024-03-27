from pydantic import BaseModel
from typing import List, Optional
from application.products import Product

class Seller(BaseModel):
    id: Optional[str] = None
    email: str
    razon_social: str
    list_products: Optional[list[Product]] = []