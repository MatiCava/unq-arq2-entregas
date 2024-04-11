from application.products import Product

def parse_product(prod: Product) -> dict:
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
    return [prod_entity(prod) for prod in prods]