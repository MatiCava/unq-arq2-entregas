from typing import Any
from domain.sales import Sale
from application.product_service import product_service
from application.user_service import user_service

class sale_service:
    def get_all() -> list:
        return Sale.get_all()

    def create(sale: Sale) -> dict: 
        new_sale = Sale.parse_sale(sale)
        error = {"error_msg": ''}
        user = user_service.get(new_sale["user_id"])
        check_stock = sale_service.validate_stock(new_sale)
        if "error_msg" not in user:
            if not check_stock["error_msg"]:
                return Sale.create(new_sale)
            else:
                error["error_msg"] = check_stock["error_msg"]    
        else:
            error["error_msg"] = user["error_msg"]
        return error

    def get(id: str) -> dict:
        res_sale = Sale.get(id)
        return sale_service.validate_sale(res_sale)
    
    def update(id: str, sale: Sale) -> dict:
        actual_sale = sale_service.get(id)
        if "error_msg" in actual_sale:
            return actual_sale
        parsed_sale = Sale.parse_sale(sale)
        dict_prods = {}
        for info in parsed_sale["products_info"]:
            if info["product_id"] in dict_prods.keys():
                dict_prods[info["product_id"]] = dict_prods[info["product_id"]] + info["quantity"]
            else:
                dict_prods.update({info["product_id"]:info["quantity"]})
        
        for info in actual_sale["products_info"]:
            if info["product_id"] in dict_prods.keys():
                actual_quantity = info["quantity"]
                update_quantity = dict_prods[info["product_id"]]
                new_quantity = actual_quantity - update_quantity
                if actual_quantity != update_quantity and new_quantity < 0:
                    check_stock = sale_service.validate_prod_stock(info["product_id"], new_quantity)
                    if check_stock["error_msg"]:
                        return check_stock
                del dict_prods[info["product_id"]]
        if dict_prods:
            for prod_id in dict_prods.keys():
                check_stock = sale_service.validate_prod_stock(prod_id, dict_prods[prod_id])
                if check_stock["error_msg"]:
                    return check_stock
        return Sale.update(id, sale, actual_sale)

    def delete(id: str) -> dict:
        deleted_sale = Sale.delete(id)
        check_sale = sale_service.validate_sale(deleted_sale)
        if "error_msg" in check_sale:
            return check_sale
        for info in check_sale["products_info"]:
            result = Sale.update_stocks(info["product_id"], info["quantity"])
            if "error_msg" in result:
                return result
        return check_sale
    
    def get_sales_related_prod_ids(prod_ids: list) -> list:
        return Sale.get_sales_related_prod_ids(prod_ids)
    
    def validate_prod_stock(prod_id: str, quantity: int) -> dict:
        error = {"error_msg": ''}
        prod = product_service.get(prod_id)
        if quantity < 0:
                quantity = quantity * -1
        if "error_msg" in prod:
            error["error_msg"] = prod["error_msg"]
        if prod["stock"] < quantity:
            error["error_msg"] = 'One of the products does not have enough stock or does not exist!'
        return error

    def validate_stock(sale: dict) -> dict:
        error = {"error_msg": ''}
        for info in sale["products_info"]:
            error = sale_service.validate_prod_stock(info["product_id"], info["quantity"])
            if error["error_msg"]:
                return error
        return error
    
    def validate_sale(sale: Sale) -> dict:
        error = {"error_msg": ''}
        if sale is not None:
            return Sale.sale_entity(sale)
        else:
            error["error_msg"] = 'Sale does not exist!'
            return error