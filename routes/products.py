from fastapi import APIRouter, Response
from application.product_service import product_service
from application.seller_service import seller_service
from application.sale_service import sale_service
from application.products import Product
from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

products_router = APIRouter()

@products_router.get('/products', response_model=list[Product], tags=["Products"])
def get_all_products(category: str | None = None, name: str | None = None, price: int | None = None, gte: int | None = None, lte: int | None = None):
    return product_service.get_all(category, name, price, gte, lte)

@products_router.post('/products', response_model=Product, tags=["Products"])
def create_product(prod: Product):
    result = seller_service.get(dict(prod)["seller_id"])
    if "error_msg" not in result:
        inserted_prod = product_service.create(prod)
        seller_service.insert_prod(inserted_prod["seller_id"], inserted_prod)
        return inserted_prod
    return Response(status_code=HTTP_400_BAD_REQUEST, headers=result)

@products_router.get('/products/{id}', response_model=Product, tags=["Products"])
def get_product(id: str):
    result = product_service.get(id)
    if "error_msg" in result:
        return Response(status_code=HTTP_400_BAD_REQUEST, headers=result)
    return result

@products_router.put('/products/{id}', response_model=Product, tags=["Products"])
def update_product(id: str, prod: Product):
    result = product_service.update(id, prod)
    if "error_msg" not in result:
        seller_service.update_prod(result["seller_id"], result)
        return result
    return Response(status_code=HTTP_400_BAD_REQUEST, headers=result)
    

@products_router.delete('/products/{id}', status_code=HTTP_204_NO_CONTENT, tags=["Products"])
def delete_product(id: str):
    sales_related = sale_service.get_sales_related_prod_ids([id])
    if not sales_related:
        result = product_service.delete(id)
        if "error_msg" not in result:
            seller_service.delete_prod(result["seller_id"], id)
            return result
        return Response(status_code=HTTP_400_BAD_REQUEST, headers=result)
    else:
        return Response(status_code=HTTP_409_CONFLICT, headers={"error_msg": "There is at least one sale related to this product!"})