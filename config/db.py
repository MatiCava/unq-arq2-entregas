from pymongo import MongoClient

client = MongoClient("mongodb+srv://matiascavallin96:cava1234@tpmeli.poj8fj2.mongodb.net/?retryWrites=true&w=majority&appName=TPMELI")

db = client.users_db
collection_users = db["users_collection"]