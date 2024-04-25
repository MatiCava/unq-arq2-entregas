from fastapi import APIRouter, Response
from application.user_service import user_service
from domain.users import User
from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

users_router = APIRouter()

@users_router.get('/users', response_model=list[User], tags=["Users"])
def get_all_users():
    return user_service.get_all()

@users_router.post('/users', response_model=User, tags=["Users"])
def create_user(user: User):
    return user_service.create(user)

@users_router.get('/users/{id}', response_model=User, tags=["Users"])
def get_user(id: str):
    result = user_service.get(id)
    if "error_msg" in result:
        return Response(status_code=HTTP_400_BAD_REQUEST, headers=result)
    return result

@users_router.put('/users/{id}', response_model=User, tags=["Users"])
def update_user(id: str, user: User):
    result = user_service.update(id, user)
    if "error_msg" in result:
        return Response(status_code=HTTP_400_BAD_REQUEST, headers=result)
    return result

@users_router.delete('/users/{id}', status_code=HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(id: str):
    result = user_service.delete(id)
    if "error_msg" in result:
        return Response(status_code=HTTP_400_BAD_REQUEST, headers=result)
    return Response(status_code=HTTP_204_NO_CONTENT)