from bson import ObjectId
from pydantic import BaseModel
from typing import Optional
from datetime import date
from adapters.sale_repo import sale_repo
from application.product_service import product_service
from application.seller_service import seller_service
from domain.sales_status import Status_Enum

class Sale_info(BaseModel):
    product_id: str
    quantity: int

class Sale(BaseModel):
    id: Optional[str] = None
    date: Optional[date]
    status: Optional[Status_Enum] = Status_Enum.created
    user_id: str
    products_info: Optional[list[Sale_info]] = []

    def get_all() -> list:
        return Sale.list_serial_sale(sale_repo.get_all())

    def create(new_sale: dict) -> dict: 
        for info in new_sale["products_info"]:
            prod = product_service.update_prod_from_sale(ObjectId(info["product_id"]), -info["quantity"])
            if prod is not None:
                seller_service.update_stock(ObjectId(prod["seller_id"]), info["product_id"], -info["quantity"])
        return Sale.sale_entity(sale_repo.create(new_sale))
    
    def get(id: str) -> 'Sale':
        return sale_repo.get(ObjectId(id))
    
    def update(id: str, sale: 'Sale', actual_sale: dict) -> dict:
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
                if actual_quantity != update_quantity:
                    new_quantity = actual_quantity - update_quantity
                    result = Sale.update_stocks(info["product_id"], new_quantity)
                    if "error_msg" in result:
                        return result
                del dict_prods[info["product_id"]]
            else:
                result = Sale.update_stocks(info["product_id"], info["quantity"])
                if "error_msg" in result:
                    return result
        if dict_prods:
            for prod_id in dict_prods.keys():
                result = Sale.update_stocks(prod_id, -dict_prods[prod_id])
                if "error_msg" in result:
                    return result
        updated_sale = sale_repo.update(ObjectId(id), parsed_sale)
        return Sale.sale_entity(updated_sale)
    
    def update_stocks(prod_id: str, quantity: int) -> dict:
        error = {}
        prod = product_service.update_prod_from_sale(ObjectId(prod_id), quantity)
        if prod is not None:
            seller_service.update_stock(ObjectId(prod["seller_id"]), prod_id, quantity)
        else:
            error.update({"error_msg": 'Product does not exist!'})
        return error

    def delete(id: str) -> dict:
        return sale_repo.delete(ObjectId(id))
    
    def get_sales_related_prod_ids(prod_ids: list) -> list:
        return sale_repo.get_sales_related_prod_ids(prod_ids)

    def parse_sale(sale: 'Sale') -> dict:
        new_sale = dict(sale)
        del new_sale["id"]
        new_sale["date"] = str(new_sale["date"])
        new_sale["products_info"] = [dict(info) for info in new_sale["products_info"]]
        return new_sale

    def sale_entity(sale) -> dict:
        res = {}
        prods = []
        if sale is not None:    
            if "products_info" in sale:
                prods = Sale.list_serial_sale_info(sale["products_info"])
            res = {
                "id": str(sale["_id"]),
                "date": sale["date"],
                "status": sale["status"],
                "user_id": sale["user_id"],
                "products_info": prods
            }
        return res

    def list_serial_sale(sales) -> list:
        return [Sale.sale_entity(sale) for sale in sales]

    def parse_sale_info(info: Sale_info) -> dict:
        res = {
            "product_id": info["product_id"],
            "quantity": info["quantity"]
        }
        return res

    def list_serial_sale_info(infos) -> list:
        return [Sale.parse_sale_info(info) for info in infos]