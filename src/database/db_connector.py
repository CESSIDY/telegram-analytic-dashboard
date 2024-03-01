from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from mongoengine import connect, disconnect, DEFAULT_CONNECTION_NAME

from utils.settings import settings


# https://docs.mongoengine.org/guide/connecting.html#guide-connecting
def connect_to_database():
    try:
        connect(db=settings.MONGODB_DATABASE,
                alias=DEFAULT_CONNECTION_NAME,
                username=settings.MONGODB_USERNAME,
                password=settings.MONGODB_PASSWORD,
                host=settings.MONGODB_HOST,
                port=settings.MONGODB_PORT,
                authentication_source='admin')
        print("Connected to MongoDB")
    except ConnectionFailure as e:
        print(f"Error connecting to MongoDB: {e}")
        raise


def disconnect_from_database():
    disconnect(alias=DEFAULT_CONNECTION_NAME)
    print("Disconnected from MongoDB")
