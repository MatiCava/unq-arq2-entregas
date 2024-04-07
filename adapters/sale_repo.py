from typing import Any
from bson import ObjectId
from pymongo import CursorType
from domain.repo_interface import IRepo
from config.db import client, collection_sales
from application.sales import Sale

class sale_repo(IRepo):
    
    def get_all() -> CursorType:
        return collection_sales.find()

    def get(id: ObjectId) -> Sale:
       return collection_sales.find_one({"_id": id})

    def create(new_sale: dict) -> Sale:
        inserted_id = collection_sales.insert_one(new_sale).inserted_id
        inserted_sale = collection_sales.find_one({"_id": inserted_id})
        return inserted_sale
    
    def update(id: ObjectId, sale: dict) -> Sale:
        collection_sales.find_one_and_update({"_id": id}, {"$set": sale})
        return collection_sales.find_one({"_id": id})
    
    def delete(id: ObjectId) -> None:
        collection_sales.find_one_and_delete({"_id": id})