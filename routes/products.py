from fastapi import APIRouter, Response
from application.product_service import product_service
from application.products import Product
from starlette.status import HTTP_204_NO_CONTENT

products_router = APIRouter()

@products_router.get('/products', response_model=list[Product], tags=["Products"])
def get_all_products():
    return product_service.get_all()

@products_router.post('/products', response_model=Product, tags=["Products"])
def create_product(prod: Product):
    return product_service.create(prod)

@products_router.get('/products/{id}', response_model=Product, tags=["Products"])
def get_product(id: str):
    return product_service.get(id)

@products_router.put('/products/{id}', response_model=Product, tags=["Products"])
def update_product(id: str, prod: Product):
    return product_service.update(id, prod)

@products_router.delete('/products/{id}', status_code=HTTP_204_NO_CONTENT, tags=["Products"])
def delete_product(id: str):
    product_service.delete(id)
    return Response(status_code=HTTP_204_NO_CONTENT)