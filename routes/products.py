from fastapi import APIRouter, Response
from application.product_service import product_service
from application.seller_service import seller_service
from application.products import Product
from starlette.status import HTTP_204_NO_CONTENT

products_router = APIRouter()

@products_router.get('/products', response_model=list[Product], tags=["Products"])
def get_all_products():
    return product_service.get_all()

@products_router.post('/products', response_model=Product, tags=["Products"])
def create_product(prod: Product):
    inserted_prod = product_service.create(prod)
    seller_service.insert_prod(inserted_prod["seller_id"], inserted_prod)
    return inserted_prod

@products_router.get('/products/{id}', response_model=Product, tags=["Products"])
def get_product(id: str):
    return product_service.get(id)

@products_router.put('/products/{id}', response_model=Product, tags=["Products"])
def update_product(id: str, prod: Product):
    updated_prod = product_service.update(id, prod)
    seller_service.update_prod(updated_prod["seller_id"], updated_prod)
    return updated_prod

@products_router.delete('/products/{id}', status_code=HTTP_204_NO_CONTENT, tags=["Products"])
def delete_product(id: str):
    product_service.delete(id)
    return Response(status_code=HTTP_204_NO_CONTENT)