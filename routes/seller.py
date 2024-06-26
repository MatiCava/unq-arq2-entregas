from fastapi import APIRouter, Response
from application.seller_service import seller_service
from application.sale_service import sale_service
from domain.sellers import Seller
from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

sellers_router = APIRouter()

@sellers_router.get('/sellers', response_model=list[Seller], tags=["Sellers"])
def get_all_sellers():
    return seller_service.get_all()

@sellers_router.post('/sellers', response_model=Seller, tags=["Sellers"])
def create_seller(seller: Seller):
    return seller_service.create(seller)

@sellers_router.get('/sellers/{id}', response_model=Seller, tags=["Sellers"])
def get_seller(id: str):
    result = seller_service.get(id)
    if "error_msg" in result:
        return Response(status_code=HTTP_400_BAD_REQUEST, headers=result)
    return result

@sellers_router.put('/sellers/{id}', response_model=Seller, tags=["Sellers"])
def update_seller(id: str, seller: Seller):
    result = seller_service.update(id, seller)
    if "error_msg" in result:
        return Response(status_code=HTTP_400_BAD_REQUEST, headers=result)
    return result

@sellers_router.delete('/sellers/{id}', status_code=HTTP_204_NO_CONTENT, tags=["Sellers"])
def delete_seller(id: str):
    seller = seller_service.get(id)
    if "error_msg" in seller:
        return Response(status_code=HTTP_400_BAD_REQUEST, headers=seller)
    prod_ids = seller_service.prods_ids_from_seller(seller)
    sales_related = sale_service.get_sales_related_prod_ids(prod_ids)
    result = seller_service.delete(id, sales_related)
    if "error_msg" in result:
        return Response(status_code=HTTP_400_BAD_REQUEST, headers=result)
    return Response(status_code=HTTP_204_NO_CONTENT)