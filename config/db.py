from pymongo import MongoClient
from config.config import settings

client = MongoClient(settings.MONGO_DB)

db = client.users_db
collection_users = db["users_collection"]
collection_products = db["products_collection"]
collection_sellers = db["sellers_collection"]
collection_sales = db["sales_collection"]