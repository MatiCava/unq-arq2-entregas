from bson import ObjectId
from application.users import User
from domain.users import parse_user, list_serial_user, user_entity
from adapters.user_repo import user_repo

class user_service:
    
    def get_all() -> list:
        return list_serial_user(user_repo.get_all())

    def create(user: User) -> dict:
        return user_entity(user_repo.create(parse_user(user)))
    
    def get(id: str) -> dict:
        return user_entity(user_repo.get(ObjectId(id)))
    
    def update(id: str, user: User) -> dict:
        return user_entity(user_repo.update(ObjectId(id), parse_user(user)))
    
    def delete(id: str) -> None:
        user_repo.delete(ObjectId(id))