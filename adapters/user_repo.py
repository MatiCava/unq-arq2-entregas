from typing import Any
from bson import ObjectId
from pymongo import CursorType
from domain.repo_interface import IRepo
from config.db import collection_users

class user_repo(IRepo):
    
    def get_all() -> CursorType:
        return collection_users.find()

    def get(id: ObjectId):
        return collection_users.find_one({"_id": id})

    def create(new_user: dict):
        inserted_id = collection_users.insert_one(new_user).inserted_id
        inserted_user = collection_users.find_one({"_id": inserted_id})
        return inserted_user
    
    def update(id: ObjectId, user: dict):
        collection_users.find_one_and_update({"_id": id}, {"$set": user})
        return collection_users.find_one({"_id": id})
    
    def delete(id: ObjectId):
        return collection_users.find_one_and_delete({"_id": id})