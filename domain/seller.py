from application.sellers import Seller
from domain.products import list_serial_prod

def parse_seller(seller: Seller) -> dict:
    new_seller = dict(seller)
    del new_seller["id"]
    return new_seller

def seller_entity(seller) -> dict:
    res = {}
    if seller is not None:    
        res = {
            "id": str(seller["_id"]),
            "email": seller["email"],
            "razon_social": seller["razon_social"],
            "list_products": list_serial_prod(seller["list_products"])
        }
    return res

def list_serial_seller(sellers) -> list:
    return [seller_entity(seller) for seller in sellers]