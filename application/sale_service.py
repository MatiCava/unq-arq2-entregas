from typing import Any
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
                prod = product_service.update_prod_from_sale(ObjectId(info["product_id"]), -info["quantity"])
                if prod is not None:
                    seller_service.update_stock(ObjectId(prod["seller_id"]), info["product_id"], -info["quantity"])
                    prods.append(prod)
            if len(new_sale["products_info"]) == len(prods):
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
        actual_sale = sale_repo.get(ObjectId(id))
        check_sale = sale_service.validate_sale(actual_sale)
        if "error_msg" in check_sale:
            return check_sale
        parsed_sale = parse_sale(sale)
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
                if actual_quantity != update_quantity:
                    new_quantity = actual_quantity - update_quantity
                    result = sale_service.update_stocks(info["product_id"], new_quantity)
                    if "error_msg" in result:
                        return result
                del dict_prods[info["product_id"]]
            else:
                result = sale_service.update_stocks(info["product_id"], info["quantity"])
                if "error_msg" in result:
                    return result
        if dict_prods:
            for prod_id in dict_prods.keys():
                result = sale_service.update_stocks(prod_id, -dict_prods[prod_id])
                if "error_msg" in result:
                    return result
        updated_sale = sale_repo.update(ObjectId(id), parsed_sale)
        return sale_entity(updated_sale)
    
    def update_stocks(prod_id: str, quantity: int) -> dict:
        error = {}
        prod = product_service.update_prod_from_sale(ObjectId(prod_id), quantity)
        if prod is not None:
            seller_service.update_stock(ObjectId(prod["seller_id"]), prod_id, quantity)
        else:
            error.update({"error_msg": 'Product does not exist!'})
        return error

    def delete(id: str) -> dict:
        sale = sale_repo.delete(ObjectId(id))
        return sale_service.validate_sale(sale)
    
    def get_sales_related_prod_ids(prod_ids: list) -> list:
        return sale_repo.get_sales_related_prod_ids(prod_ids)
    
    def validate_sale(sale: Sale) -> dict:
        error = {"error_msg": ''}
        if sale is not None:
            return sale_entity(sale)
        else:
            error["error_msg"] = 'Sale does not exist!'
            return error