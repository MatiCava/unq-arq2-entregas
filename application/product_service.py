from bson import ObjectId
from application.products import Product
from domain.products import list_serial_prod, prod_entity, parse_product
from adapters.product_repo import product_repo

class product_service:
    def get_all() -> list:
        return list_serial_prod(product_repo.get_all())

    def create(prod: Product) -> dict:
        return prod_entity(product_repo.create(parse_product(prod)))
    
    def get(id: str) -> dict:
        return prod_entity(product_repo.get(ObjectId(id)))
    
    def update(id: str, prod: Product) -> dict:
        return prod_entity(product_repo.update(ObjectId(id), parse_product(prod)))
    
    def delete(id: str) -> None:
        product_repo.delete(ObjectId(id))