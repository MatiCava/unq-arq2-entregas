from bson import ObjectId
from domain.products import Product

class product_service:
    def get_all(category: str, name: str, price: int, gte: int, lte: int) -> list:
        return Product.get_all(category, name, price, gte, lte)

    def create(prod: Product) -> dict: 
        return Product.create(prod)
    
    def get(id: str) -> dict:
        res_prod = Product.get(id)
        return product_service.validate_product(res_prod)
    
    def update(id: str, prod: Product) -> dict:
        res_prod = Product.update(id, prod)
        return product_service.validate_product(res_prod)
    
    def delete(id: str, sales_related: list) -> dict:
        error = {"error_msg": ''}
        if not sales_related:
            res_prod = Product.delete(id)
            return product_service.validate_product(res_prod)
        else:
            error["error_msg"] = 'There is at least one sale related to this seller!'
            return error

    def create_many(prods: list[Product], seller_id: str) -> list[Product]:
        return Product.create_many(prods, seller_id)
    
    def delete_all(seller_id: str) -> None:
        Product.delete_all(seller_id)

    def update_prod_from_sale(prod_id: ObjectId, quantity: int) -> Product:
        return Product.update_prod_from_sale(prod_id, quantity)
    
    def validate_product(prod: Product) -> dict:
        error = {"error_msg": ''}
        if prod is not None:
            return Product.prod_entity(prod)
        else:
            error["error_msg"] = 'Product does not exist!'
            return error