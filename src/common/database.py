import os
from pymongo import MongoClient
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MongoDBConnection:
    def __init__(self, env_path="/usr/src/app/.env", db_name=None, collection_name=None):
        load_dotenv(dotenv_path=env_path)
        self.mongo_uri = os.getenv("MONGO_URI")
        self.mongo_db = db_name or os.getenv("MONGO_DB")
        self.mongo_collection = collection_name or os.getenv("MONGO_COLLECTION")

        # Validate environment variables
        if not all([self.mongo_uri, self.mongo_db, self.mongo_collection]):
            logger.error("Missing MongoDB environment variables. Check your .env file.")
            raise ValueError("Missing MongoDB environment variables")

    def get_collection(self):
        client = MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        collection = db[self.mongo_collection]
        return collection, client