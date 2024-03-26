from typing import Any
from bson import ObjectId
from pymongo import CursorType
from application.products import Product

class IProduct_repo:

    def get_all() -> CursorType:
        pass

    def get(id: ObjectId) -> Product:
        pass

    def create(new_prod: dict) -> Product:
        pass

    def update(id: ObjectId, prod: dict) -> Product:
        pass

    def delete(id: ObjectId) -> None:
        pass