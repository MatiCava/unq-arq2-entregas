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
        prod = product_repo.get(ObjectId(id))
        return product_service.validate_product(prod)
    
    def update(id: str, prod: Product) -> dict:
        updated_prod = product_repo.update(ObjectId(id), parse_product(prod))
        return product_service.validate_product(updated_prod)
    
    def delete(id: str) -> dict:
        prod = product_repo.delete(ObjectId(id))
        return product_service.validate_product(prod)

    def create_many(prods: list[Product], seller_id: str) -> list[Product]:
        new_products = []
        for prod in prods:
            parsed_prod = parse_product(prod)
            parsed_prod["seller_id"] = seller_id
            new_products.append(parsed_prod)
        return list_serial_prod(product_repo.create_many(new_products))
    
    def delete_all(seller_id: str) -> None:
        product_repo.delete_all(seller_id)

    def update_prod_from_sale(prod_id: ObjectId, quantity: int) -> Product:
        return product_repo.update_prod_from_sale(prod_id, quantity)
    
    def validate_product(prod: Product) -> dict:
        error = {"error_msg": ''}
        if prod is not None:
            return prod_entity(prod)
        else:
            error["error_msg"] = 'Product does not exist!'
            return error