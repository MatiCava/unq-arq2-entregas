from application.users import User

def parse_user(user: User) -> dict:
    return dict(user)

def user_entity(user) -> dict:
    res = {}
    if user is not None:    
        res = {
            "id": str(user["_id"]),
            "name": user["name"],
            "lastname": user["lastname"],
            "email": user["email"]
        }
    return res

def list_serial_user(users) -> list:
    return [user_entity(user) for user in users]
    