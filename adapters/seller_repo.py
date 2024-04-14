from typing import Any
from bson import ObjectId
from pymongo import CursorType
from domain.repo_interface import IRepo
from config.db import collection_sellers
from application.sellers import Seller

class seller_repo(IRepo):
    
    def get_all() -> CursorType:
        return collection_sellers.find()

    def get(id: ObjectId) -> Seller:
       return collection_sellers.find_one({"_id": id})

    def create(new_seller: dict) -> Seller:
        inserted_id = collection_sellers.insert_one(new_seller).inserted_id
        inserted_seller = collection_sellers.find_one({"_id": inserted_id})
        return inserted_seller
    
    def update(id: ObjectId, seller: dict) -> Seller:
        collection_sellers.find_one_and_update({"_id": id}, {"$set": seller})
        return collection_sellers.find_one({"_id": id})
    
    def delete(id: ObjectId) -> Seller:
        return collection_sellers.find_one_and_delete({"_id": id})

    def insert_prod(id: ObjectId, prod: dict) -> None:
        collection_sellers.update_one({"_id": id}, {"$push": {"list_products": prod}})
    
    def delete_prod(id: ObjectId, prod_id: str) -> None:
        collection_sellers.update_one({"_id": id}, {"$pull": {"list_products": {"id": prod_id}}})

    def update_prod(id: ObjectId, prod: dict) -> None:
        collection_sellers.update_many({"_id": id}, {"$set": {"list_products.$[element]": prod}}, False, array_filters=[{"element.id": prod["id"]}])
    
    def update_stock(id: ObjectId, prod_id: str, quantity: int) -> None:
        query = {"element.id": prod_id}
        if quantity < 0:
            check = quantity * -1
            query = {"element.id": prod_id, "element.stock": {"$gte": check}}
        collection_sellers.update_many({"_id": id}, {"$inc": {"list_products.$[element].stock": quantity}}, False, array_filters=[query])