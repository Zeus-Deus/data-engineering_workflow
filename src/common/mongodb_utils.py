import os
import pymongo
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_mongo_client():
    try:
        mongo_uri = os.getenv("MONGO_URI")
        client = pymongo.MongoClient(mongo_uri)
        return client
    except pymongo.errors.ConnectionError as e:
        logging.error(f"Error connecting to MongoDB: {e}")
        return None
    
def extract_data_from_mongodb(database_name, collection_name):
    client = get_mongo_client()
    if client is None:
        return []
    
    try:
        db = client[database_name]
        collection = db[collection_name]
        data = list(collection.find({}))  # Use an empty query to fetch all data
        return data
    except Exception as e:
        logging.error(f"Error extracting data from MongoDB: {e}")
        return []
    finally:
        if client:
            client.close()

