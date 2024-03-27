from typing import Any
from bson import ObjectId
from pymongo import CursorType

class IRepo:

    def get_all() -> CursorType:
        pass

    def get(id: ObjectId) -> Any:
        pass

    def create(new_obj: dict) -> Any:
        pass

    def update(id: ObjectId, obj: dict) -> Any:
        pass

    def delete(id: ObjectId) -> None:
        pass