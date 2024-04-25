from bson import ObjectId
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from adapters.product_repo import product_repo
from domain.products_category import Category_Enum

class Product(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    category: Category_Enum
    price: int = Field(ge=0)
    stock: int = Field(ge=0)
    seller_id: str

    def get_all(category: str, name: str, price: int, gte: int, lte: int) -> list:
        query = {}
        if price:
            query.update({"price": price})
        if gte:
            if lte:
                check = { "$gte": gte, "$lte": lte }
            else:
                check = { "$gte": gte}
            query.update({"price": check})
        if lte:
            if gte:
                check = { "$gte": gte, "$lte": lte }
            else:
                check = { "$lte": lte}
            query.update({"price": check})
        if category:
            query.update({"category": category})
        if name:
            query.update({"name": {"$regex": '.*' + name + '.*'}})
        return Product.list_serial_prod(product_repo.get_all(query))
    
    def create(prod: 'Product') -> dict:
        return Product.prod_entity(product_repo.create(Product.parse_product(prod)))
    
    def get(id: str) -> 'Product':
        return product_repo.get(ObjectId(id))
    
    def update(id: str, prod: 'Product') -> 'Product':
        return product_repo.update(ObjectId(id), Product.parse_product(prod))
    
    def delete(id: str) -> 'Product':
        return product_repo.delete(ObjectId(id))
    
    def create_many(prods: list['Product'], seller_id: str) -> list['Product']:
        new_products = []
        for prod in prods:
            parsed_prod = Product.parse_product(prod)
            parsed_prod["seller_id"] = seller_id
            new_products.append(parsed_prod)
        return Product.list_serial_prod(product_repo.create_many(new_products))
    
    def delete_all(seller_id: str) -> None:
        product_repo.delete_all(seller_id)

    def update_prod_from_sale(prod_id: ObjectId, quantity: int) -> 'Product':
        return product_repo.update_prod_from_sale(prod_id, quantity)

    def parse_product(prod: 'Product') -> dict:
        new_prod = dict(prod)
        del new_prod["id"]
        return new_prod

    def prod_entity(prod) -> dict:
        res = {}
        prod_id = ''
        if prod is not None:
            if "_id" in prod:
                prod_id = str(prod["_id"])
            else:
                prod_id = prod["id"]
            res = {
                "id": prod_id,
                "name": prod["name"],
                "description": prod["description"],
                "category": prod["category"],
                "price": prod["price"],
                "stock": prod["stock"],
                "seller_id": prod["seller_id"]
            }
        return res

    def list_serial_prod(prods) -> list:
        return [Product.prod_entity(prod) for prod in prods]