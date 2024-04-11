from typing import Any
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
            return seller_repo.update(ObjectId(parsed_inserted["id"]), parsed_inserted)
        return parsed_inserted
    
    def get(id: str) -> dict:
        seller = seller_repo.get(ObjectId(id))
        return seller_service.validate_seller(seller)
    
    def update(id: str, seller: Seller) -> dict:
        new_seller = parse_seller(seller)
        del new_seller["list_products"]
        seller = seller_repo.update(ObjectId(id), new_seller)
        return seller_service.validate_seller(seller)

    def delete(id: str) -> dict:
        seller = seller_repo.delete(ObjectId(id))
        result = seller_service.validate_seller(seller)
        if "error_msg" not in result:
            product_service.delete_all(id)
        return result

    def insert_prod(id: str, prod: dict) -> None:
        seller_repo.insert_prod(ObjectId(id), prod)

    def update_prod(id: str, prod: dict) -> None:
        seller_repo.update_prod(ObjectId(id), prod)

    def delete_prod(id: str, prod_id: str) -> None:
        seller_repo.delete_prod(ObjectId(id), prod_id)

    def update_stock(id: ObjectId, prod_id: str, quantity: int) -> None:
        seller_repo.update_stock(id, prod_id, quantity)

    def prods_ids_from_seller(seller: Seller) -> list:
        prod_ids = []
        for prod in seller["list_products"]:
            prod_ids.append(prod["id"])
        return prod_ids
    
    def validate_seller(seller: Seller) -> dict:
        error = {"error_msg": ''}
        if seller is not None:
            return seller_entity(seller)
        else:
            error["error_msg"] = 'Seller does not exist!'
            return error