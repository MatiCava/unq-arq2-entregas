from fastapi import APIRouter, Response
from application.seller_service import seller_service
from application.sellers import Seller
from starlette.status import HTTP_204_NO_CONTENT

sellers_router = APIRouter()

@sellers_router.get('/sellers', response_model=list[Seller], tags=["Sellers"])
def get_all_sellers():
    return seller_service.get_all()

@sellers_router.post('/sellers', response_model=Seller, tags=["Sellers"])
def create_seller(seller: Seller):
    return seller_service.create(seller)

@sellers_router.get('/sellers/{id}', response_model=Seller, tags=["Sellers"])
def get_seller(id: str):
    return seller_service.get(id)

@sellers_router.put('/sellers/{id}', response_model=Seller, tags=["Sellers"])
def update_seller(id: str, prod: Seller):
    return seller_service.update(id, prod)

@sellers_router.delete('/sellers/{id}', status_code=HTTP_204_NO_CONTENT, tags=["Sellers"])
def delete_seller(id: str):
    seller_service.delete(id)
    return Response(status_code=HTTP_204_NO_CONTENT)