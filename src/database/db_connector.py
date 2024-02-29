from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from utils.settings import settings


def connect_to_database():
    try:
        client = MongoClient(settings.MONGODB_URI)
        db = client.get_database()
        print("Connected to MongoDB")
        return db
    except ConnectionFailure as e:
        print(f"Error connecting to MongoDB: {e}")
        raise
