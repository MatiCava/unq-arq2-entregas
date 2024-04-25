from domain.users import User

class user_service:
    
    def get_all() -> list:
        return User.get_all()

    def create(user: User) -> dict:
        res_user = User.create(user)
        return user_service.validate_user(res_user)
    
    def get(id: str) -> dict:
        res_user = User.get(id)
        return user_service.validate_user(res_user)
    
    def update(id: str, user: User) -> dict:
        res_user = User.update(id, user)
        return user_service.validate_user(res_user)
    
    def delete(id: str) -> dict:
        res_user = User.delete(id)
        return user_service.validate_user(res_user)

    def validate_user(user: User) -> dict:
        error = {"error_msg": ''}
        if user is not None:
            return User.user_entity(user)
        else:
            error["error_msg"] = 'User does not exist!'
            return error