from bson import ObjectId
from pydantic import BaseModel
from typing import List, Optional
from adapters.seller_repo import seller_repo
from application.product_service import product_service
from domain.products import Product

class Seller(BaseModel):
    id: Optional[str] = None
    email: str
    razon_social: str
    list_products: Optional[list[Product]] = []

    def get_all() -> list:
        return Seller.list_serial_seller(seller_repo.get_all())

    def create(seller: 'Seller') -> dict:
        new_seller = Seller.parse_seller(seller)
        prods_insert = new_seller["list_products"]
        del new_seller["list_products"]
        parsed_inserted = Seller.seller_entity(seller_repo.create(new_seller))
        if prods_insert:
            inserted_products = product_service.create_many(prods_insert, parsed_inserted["id"])
            parsed_inserted["list_products"] = inserted_products
            return seller_repo.update(ObjectId(parsed_inserted["id"]), parsed_inserted)
        return parsed_inserted
    
    def get(id: str) -> dict:
        return seller_repo.get(ObjectId(id))
    
    def update(id: str, seller: 'Seller') -> 'Seller':
        new_seller = Seller.parse_seller(seller)
        del new_seller["list_products"]
        seller = seller_repo.update(ObjectId(id), new_seller)
        return seller

    def delete(id: str) -> 'Seller':
        return seller_repo.delete(ObjectId(id))
    
    def delete_prods(id: str) -> None:
        product_service.delete_all(id)

    def insert_prod(id: str, prod: dict) -> None:
        seller_repo.insert_prod(ObjectId(id), prod)

    def update_prod(id: str, prod: dict) -> None:
        seller_repo.update_prod(ObjectId(id), prod)

    def delete_prod(id: str, prod_id: str) -> None:
        seller_repo.delete_prod(ObjectId(id), prod_id)

    def update_stock(id: ObjectId, prod_id: str, quantity: int) -> None:
        seller_repo.update_stock(id, prod_id, quantity)
    
    def parse_seller(seller: 'Seller') -> dict:
        new_seller = dict(seller)
        del new_seller["id"]
        return new_seller

    def seller_entity(seller) -> dict:
        res = {}
        prods = []
        if seller is not None:    
            if "list_products" in seller:
                prods = Product.list_serial_prod(seller["list_products"])
            res = {
                "id": str(seller["_id"]),
                "email": seller["email"],
                "razon_social": seller["razon_social"],
                "list_products": prods
            }
        return res

    def list_serial_seller(sellers) -> list:
        return [Seller.seller_entity(seller) for seller in sellers]