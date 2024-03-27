from typing import Any
from bson import ObjectId
from pymongo import CursorType
from domain.repo_interface import IRepo
from config.db import client, collection_sellers
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
        #hay que evitar que se pisen valores que son opcionales
        collection_sellers.find_one_and_update({"_id": id}, {"$set": seller})
        return collection_sellers.find_one({"_id": id})
    
    def delete(id: ObjectId) -> None:
        #hay que eliminar productos tambien
        collection_sellers.find_one_and_delete({"_id": id})