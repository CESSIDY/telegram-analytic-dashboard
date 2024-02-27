from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config.settings import MONGODB_URI


def connect_to_database():
    try:
        client = MongoClient(MONGODB_URI)
        db = client.get_database()
        print("Connected to MongoDB")
        return db
    except ConnectionFailure as e:
        print(f"Error connecting to MongoDB: {e}")
        raise
