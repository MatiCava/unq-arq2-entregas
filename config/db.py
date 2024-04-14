from pymongo import MongoClient
import pymongo
from config.config import settings

client = None
db = None

def get_client():
    global client
    mongodb_string = settings.MONGO_DB
    if '?retryWrites' in settings.MONGO_DB:
        mongodb_string = mongodb_string.split('?')[0]
    if client is None:
        client = MongoClient(mongodb_string)
    return client

def mongo_db(client):
    global db
    #se podria cambiar a meli_db y sacar users_db
    if db is None:
        return client.users_db
        #return client.test_db
    return client.test_db

client = get_client()
db = mongo_db(client)
collection_users = db["users_collection"]
collection_products = db["products_collection"]
collection_sellers = db["sellers_collection"]
collection_sales = db["sales_collection"]