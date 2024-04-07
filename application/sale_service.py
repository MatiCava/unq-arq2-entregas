from bson import ObjectId
from application.sales import Sale
from domain.sales import list_serial_sale, sale_entity, parse_sale
from adapters.sale_repo import sale_repo
from application.product_service import product_service
from application.seller_service import seller_service

class sale_service:
    def get_all() -> list:
        return list_serial_sale(sale_repo.get_all())

    def create(sale: Sale) -> dict: 
        #hay que checkear que exista el prod id que mandan
        #despues de checkear si existe lo actualizamos
        #agregar que valores no se vayan negativos de stock
        new_sale = parse_sale(sale)
        parsed_inserted = sale_entity(sale_repo.create(new_sale))
        for info in parsed_inserted["products_info"]:
            prod = product_service.update_prod_from_sale(ObjectId(info["product_id"]), info["quantity"])
            seller_service.update_stock(ObjectId(prod["seller_id"]), info["product_id"], info["quantity"])
        return parsed_inserted
    
    def get(id: str) -> dict:
        return sale_entity(sale_repo.get(ObjectId(id)))
    
    def update(id: str, sale: Sale) -> dict:
        return sale_entity(sale_repo.update(ObjectId(id), parse_sale(sale)))
    
    def delete(id: str) -> None:
        sale_repo.delete(ObjectId(id))