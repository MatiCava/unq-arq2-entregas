from typing import Any
from bson import ObjectId
from pymongo import CursorType
from domain.user_repo_interface import IUser_repo
from config.db import client, collection_users
from application.users import User

class user_repo(IUser_repo):
    
    def get_all() -> CursorType:
        return collection_users.find()

    def get(id: ObjectId) -> User:
       return collection_users.find_one({"_id": id})

    def create(new_user: dict) -> User:
        inserted_id = collection_users.insert_one(new_user).inserted_id
        inserted_user = collection_users.find_one({"_id": inserted_id})
        return inserted_user
    
    def update(id: ObjectId, user: dict) -> User:
        collection_users.find_one_and_update({"_id": id}, {"$set": user})
        return collection_users.find_one({"_id": id})
    
    def delete(id: ObjectId) -> None:
        collection_users.find_one_and_delete({"_id": id})