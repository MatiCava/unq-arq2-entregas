from application.sales import Sale, Sale_info

def parse_sale(sale: Sale) -> dict:
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
            prods = list_serial_sale_info(sale["products_info"])
        res = {
            "id": str(sale["_id"]),
            "date": sale["date"],
            "status": sale["status"],
            "user_id": sale["user_id"],
            "products_info": prods
        }
    return res

def list_serial_sale(sales) -> list:
    return [sale_entity(sale) for sale in sales]

def parse_sale_info(info: Sale_info) -> dict:
    res = {
         "product_id": info["product_id"],
         "quantity": info["quantity"]
    }
    return res

def list_serial_sale_info(infos) -> list:
    return [parse_sale_info(info) for info in infos]