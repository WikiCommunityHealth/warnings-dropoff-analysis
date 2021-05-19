from bson import ObjectId
from pymongo.database import Database
from .. import UserMetrics

class CollectionService:
    """
    MongoDB collection helper
    """
    def __init__(self, database: Database, collection_name: str) -> None:
        self.service = database[collection_name]

    @property
    def num_documents(self) -> int:
        return self.service.count_documents({})

    def insert_one(self, user: UserMetrics) -> ObjectId:
        return self.service.insert_one(user.json).inserted_id