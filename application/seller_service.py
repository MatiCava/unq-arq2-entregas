from typing import Any
from bson import ObjectId
from domain.sellers import Seller

class seller_service:
    def get_all() -> list:
        return Seller.get_all()

    def create(seller: Seller) -> dict:
        return Seller.create(seller)
    
    def get(id: str) -> dict:
        res_seller = Seller.get(id)
        return seller_service.validate_seller(res_seller)
    
    def update(id: str, seller: Seller) -> dict:
        res_seller = Seller.update(id, seller)
        return seller_service.validate_seller(res_seller)

    def delete(id: str, sales_related: list) -> dict:
        error = {"error_msg": ''}
        if not sales_related:
            res_seller = Seller.delete(id)
            result = seller_service.validate_seller(res_seller)
            if "error_msg" not in result:
                Seller.delete_prods(id)
            return result
        else:
            error["error_msg"] = 'There is at least one sale related to this seller!'
            return error

    def insert_prod(id: str, prod: dict) -> None:
        Seller.insert_prod(id, prod)

    def update_prod(id: str, prod: dict) -> None:
        Seller.update_prod(id, prod)

    def delete_prod(id: str, prod_id: str) -> None:
        Seller.delete_prod(id, prod_id)

    def update_stock(id: ObjectId, prod_id: str, quantity: int) -> None:
        Seller.update_stock(id, prod_id, quantity)

    def prods_ids_from_seller(seller: Seller) -> list:
        prod_ids = []
        for prod in seller["list_products"]:
            prod_ids.append(prod["id"])
        return prod_ids
    
    def validate_seller(seller: Seller) -> dict:
        error = {"error_msg": ''}
        if seller is not None:
            return Seller.seller_entity(seller)
        else:
            error["error_msg"] = 'Seller does not exist!'
            return error