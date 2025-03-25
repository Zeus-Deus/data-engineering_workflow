import sys
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="/usr/src/app/.env")

# Set up the Python path to include the common module
sys.path.append(os.getenv("PYTHONPATH"))

from src.common.mongodb_utils import extract_data_from_mongodb
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_raw_data():
    try:
        database_name = os.getenv("MONGO_DB_REASONING_ERRORS")
        collection_name = os.getenv("MONGO_COLLECTION_REASONING_ERRORS")
        data = extract_data_from_mongodb(database_name, collection_name)
        return data
    except Exception as e:
        logging.error(f"Error getting raw data: {e}")
        return []

if __name__ == "__main__":
    data = get_raw_data()

