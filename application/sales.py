from pydantic import BaseModel
from typing import Optional
from datetime import date
from application.sales_status import Status_Enum

class Sale_info(BaseModel):
    product_id: str
    quantity: int

class Sale(BaseModel):
    id: Optional[str] = None
    date: Optional[date]
    status: Optional[Status_Enum] = Status_Enum.created
    user_id: str
    products_info: Optional[list[Sale_info]] = []