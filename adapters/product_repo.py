from typing import Any
from bson import ObjectId
from pymongo import CursorType
from domain.repo_interface import IRepo
from config.db import client, collection_products
from application.products import Product

class product_repo(IRepo):
    
    def get_all(query: dict) -> CursorType:
        return collection_products.find(query)

    def get(id: ObjectId) -> Product:
       return collection_products.find_one({"_id": id})

    def create(new_prod: dict) -> Product:
        inserted_id = collection_products.insert_one(new_prod).inserted_id
        inserted_prod = collection_products.find_one({"_id": inserted_id})
        return inserted_prod
    
    def update(id: ObjectId, prod: dict) -> Product:
        collection_products.find_one_and_update({"_id": id}, {"$set": prod})
        return collection_products.find_one({"_id": id})
    
    def delete(id: ObjectId) -> Product:
        return collection_products.find_one_and_delete({"_id": id})

    def create_many(new_prods: dict) -> list[Product]:
        inserted_ids = collection_products.insert_many(new_prods).inserted_ids
        return list(collection_products.find({"_id": {"$in": inserted_ids}}))

    def delete_all(seller_id: str) -> None:
        collection_products.delete_many({"seller_id": seller_id})

    def update_prod_from_sale(prod_id: ObjectId, quantity: int) -> Product:
        query = {}
        if quantity < 0:
            check = quantity * -1
            query = {"stock": {"$gte": check}}
        return collection_products.find_one_and_update({"$and": [{"_id": prod_id}, query]}, {"$inc": {"stock": quantity}})
    