from bson import ObjectId
from pydantic import BaseModel
from typing import Optional
from adapters.user_repo import user_repo

class User(BaseModel):
    id: Optional[str] = None
    name: str
    lastname: str
    email: str

    def get_all() -> list:
        return User.list_serial_user(user_repo.get_all())

    def create(user: 'User') -> dict:
        return User.user_entity(user_repo.create(User.parse_user(user)))
    
    def get(id: str) -> 'User':
        return user_repo.get(ObjectId(id))
    
    def update(id: str, user: 'User') -> dict:
        return user_repo.update(ObjectId(id), User.parse_user(user))
    
    def delete(id: str) -> dict:
        return user_repo.delete(ObjectId(id))
    
    def parse_user(user: 'User') -> dict:
        new_user = dict(user)
        del new_user["id"]
        return new_user

    def user_entity(user) -> dict:
        res = {}
        if user is not None:    
            if "_id" in user:
                user_id = str(user["_id"])
            else:
                user_id = user["id"]
            res = {
                "id": user_id,
                "name": user["name"],
                "lastname": user["lastname"],
                "email": user["email"]
            }
        return res

    def list_serial_user(users) -> list:
        return [User.user_entity(user) for user in users]