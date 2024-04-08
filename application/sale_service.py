from bson import ObjectId
from application.sales import Sale
from domain.sales import list_serial_sale, sale_entity, parse_sale
from adapters.sale_repo import sale_repo
from application.product_service import product_service
from application.seller_service import seller_service
from application.user_service import user_service

class sale_service:
    def get_all() -> list:
        return list_serial_sale(sale_repo.get_all())

    def create(sale: Sale) -> dict: 
        new_sale = parse_sale(sale)
        prods = []
        error = {"error_msg": ''}
        user = user_service.get(new_sale["user_id"])
        if "error_msg" not in user:
            for info in new_sale["products_info"]:
                prod = product_service.update_prod_from_sale(ObjectId(info["product_id"]), info["quantity"])
                if prod is not None:
                    seller_service.update_stock(ObjectId(prod["seller_id"]), info["product_id"], info["quantity"])
                    prods.append(prod)
            
            if len(new_sale["products_info"]) == prods:
                return sale_entity(sale_repo.create(new_sale))
            else:
                error["error_msg"] = 'One of the products does not have enough stock or does not exist!'
        else:
            error["error_msg"] = user["error_msg"]
        return error
    
    def get(id: str) -> dict:
        sale = sale_repo.get(ObjectId(id))
        return sale_service.validate_sale(sale)
    
    def update(id: str, sale: Sale) -> dict:
        sale = sale_repo.update(ObjectId(id), parse_sale(sale))
        return sale_service.validate_sale(sale)
    
    def delete(id: str) -> dict:
        sale = sale_repo.delete(ObjectId(id))
        return sale_service.validate_sale(sale)
    
    def validate_sale(sale: Sale) -> dict:
        error = {"error_msg": ''}
        if sale is not None:
            return sale_entity(sale)
        else:
            error["error_msg"] = 'Sale does not exist!'
            return error