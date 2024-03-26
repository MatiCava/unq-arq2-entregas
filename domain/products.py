from application.products import Product

def parse_product(prod: Product) -> dict:
    new_prod = dict(prod)
    del new_prod["id"]
    return new_prod

def prod_entity(prod) -> dict:
    res = {}
    #falta seller id
    if prod is not None:    
        res = {
            "id": str(prod["_id"]),
            "name": prod["name"],
            "description": prod["description"],
            "price": prod["price"],
            "stock": prod["stock"]
        }
    return res

def list_serial_prod(prods) -> list:
    return [prod_entity(prod) for prod in prods]