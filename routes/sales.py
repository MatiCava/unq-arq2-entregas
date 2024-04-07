from fastapi import APIRouter, Response
from application.sale_service import sale_service
from application.sales import Sale
from starlette.status import HTTP_204_NO_CONTENT

sales_router = APIRouter()

@sales_router.get('/sales', response_model=list[Sale], tags=["Sales"])
def get_all_sales():
    return sale_service.get_all()

@sales_router.post('/sales', response_model=Sale, tags=["Sales"])
def create_sale(sale: Sale):
    return sale_service.create(sale)

@sales_router.get('/sales/{id}', response_model=Sale, tags=["Sales"])
def get_sale(id: str):
    return sale_service.get(id)

@sales_router.put('/sales/{id}', response_model=Sale, tags=["Sales"])
def update_sale(id: str, sale: Sale):
    return sale_service.update(id, sale)

@sales_router.delete('/sales/{id}', status_code=HTTP_204_NO_CONTENT, tags=["Sales"])
def delete_sale(id: str):
    sale_service.delete(id)
    return Response(status_code=HTTP_204_NO_CONTENT)