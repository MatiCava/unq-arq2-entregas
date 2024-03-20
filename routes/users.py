from fastapi import APIRouter, Response
from config.db import client, collection_users
from schemas.users import user_entity, list_serial_user
from models.users import User
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

users_router = APIRouter()

@users_router.get('/users', response_model=list[User], tags=["Users"])
def get_all_users():
    return list_serial_user(collection_users.find())

@users_router.post('/users', response_model=User, tags=["Users"])
def create_user(user: User):
    new_user = dict(user)
    inserted_id = collection_users.insert_one(new_user).inserted_id
    inserted_user = collection_users.find_one({"_id": inserted_id})
    return user_entity(inserted_user)

@users_router.get('/users/{id}', response_model=User, tags=["Users"])
def get_user(id: str):
    return user_entity(collection_users.find_one({"_id": ObjectId(id)}))

@users_router.put('/users/{id}', response_model=User, tags=["Users"])
def update_user(id: str, user: User):
    collection_users.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
    return user_entity(collection_users.find_one({"_id": ObjectId(id)}))

@users_router.delete('/users/{id}', status_code=HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(id: str):
    user_entity(collection_users.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)