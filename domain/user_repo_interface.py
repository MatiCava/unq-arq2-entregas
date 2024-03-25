from typing import Any
from bson import ObjectId
from pymongo import CursorType
from application.users import User

class IUser_repo:

    def get_all() -> CursorType:
        pass

    def get(id: ObjectId) -> User:
        pass

    def create(new_user: dict) -> User:
        pass

    def update(id: ObjectId, user: dict) -> User:
        pass

    def delete(id: ObjectId) -> None:
        pass