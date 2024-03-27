from bson import ObjectId
from application.sellers import Seller
from application.product_service import product_service
from domain.seller import list_serial_seller, seller_entity, parse_seller
from adapters.seller_repo import seller_repo

class seller_service:
    def get_all() -> list:
        return list_serial_seller(seller_repo.get_all())

    def create(seller: Seller) -> dict:
        new_seller = parse_seller(seller)
        if new_seller["list_products"]:
            inserted_products = product_service.create_many(new_seller["list_products"])
            new_seller["list_products"] = inserted_products
        #faltaria actualizar seller id en los productos despues de crear el seller
        return seller_entity(seller_repo.create(new_seller))
    
    def get(id: str) -> dict:
        return seller_entity(seller_repo.get(ObjectId(id)))
    
    def update(id: str, seller: Seller) -> dict:
        new_seller = parse_seller(seller)
        #si viene vacio no actualizar
        #si vienen productos hay que checkear si existen actualizar si actualiza solo 1 de 3 por ej habria que guardar sin pisar, 
        #sino crearlos y agregarlos sin pisar si ya tenia productos existentes
        if not new_seller["list_products"]:
            NotImplemented
        return seller_entity(seller_repo.update(ObjectId(id), new_seller))
    
    def delete(id: str) -> None:
        #borrar productos del seller tambien
        seller_repo.delete(ObjectId(id))