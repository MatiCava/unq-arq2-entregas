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
        prods_insert = new_seller["list_products"]
        del new_seller["list_products"]
        parsed_inserted = seller_entity(seller_repo.create(new_seller))
        if prods_insert:
            inserted_products = product_service.create_many(prods_insert, parsed_inserted["id"])
            parsed_inserted["list_products"] = inserted_products
            return seller_service.update(parsed_inserted["id"], parsed_inserted)
        return parsed_inserted
    
    def get(id: str) -> dict:
        return seller_entity(seller_repo.get(ObjectId(id)))
    
    def update(id: str, seller: Seller) -> dict:
        new_seller = parse_seller(seller)
        #si viene vacio no actualizar
        #tambien confirmar que si no se manda uno de los valores opcionales no pise los que ya tiene en db
        if not new_seller["list_products"]:
            NotImplemented
        return seller_entity(seller_repo.update(ObjectId(id), new_seller))

    def delete(id: str) -> None:
        #borrar productos del seller tambien
        seller_repo.delete(ObjectId(id))