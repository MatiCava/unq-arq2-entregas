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
        user = user_repo.get(ObjectId(id))
        return user_service.validate_user(user)
    
    def update(id: str, user: User) -> dict:
        user = user_repo.update(ObjectId(id), parse_user(user))
        return user_service.validate_user(user)
    
    def delete(id: str) -> dict:
        user = user_repo.delete(ObjectId(id))
        return user_service.validate_user(user)

    def validate_user(user: User) -> dict:
        error = {"error_msg": ''}
        if user is not None:
            return user_entity(user)
        else:
            error["error_msg"] = 'User does not exist!'
            return error