from pymongo import MongoClient
from .collection import CollectionService

class DatabaseService:
    """
    MongoDB connection helper
    """
    def __init__(self, connection_string: str, database_name: str, collection_name: str) -> None:
        self.connection_string = connection_string
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = MongoClient(self.connection_string)
        self.db = self.client.get_database(self.database_name)
        self.collection = CollectionService(self.db, self.collection_name)