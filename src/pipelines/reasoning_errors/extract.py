import sys
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="/usr/src/app/.env")  # Make sure your .env file is secure and not committed to version control

# Set up the Python path to include the common module
sys.path.append(os.getenv("PYTHONPATH"))

from src.common.mongodb_utils import extract_data_from_mongodb
from src.common.azure_blob_storage import get_blob_content
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function to get raw data from either Azure Blob Storage or MongoDB depending on the environment variable 
def get_raw_data():
    use_azure = os.getenv("USE_AZURE", "False").lower() in ("true", "1")
    if use_azure:
        logger.info("Using Azure Blob Storage for raw data extraction.")
        # Retrieve blob name from environment variables and ensure it's set
        blob_name = os.getenv("AZURE_BLOB_NAME")
        if not blob_name:
            logger.error("AZURE_BLOB_NAME is not set in the environment.")
            raise ValueError("AZURE_BLOB_NAME is required and not set.")
        data = get_blob_content(blob_name)
        return data if data else []
    else:
        logger.info("Using MongoDB for raw data extraction.")
        database_name = os.getenv("MONGO_DB_REASONING_ERRORS")
        collection_name = os.getenv("MONGO_COLLECTION_REASONING_ERRORS")
        if not database_name or not collection_name:
            logger.error("MongoDB database or collection name is not set in the environment.")
            raise ValueError("MongoDB database and collection names are required.")
        data = extract_data_from_mongodb(database_name, collection_name)
        return data

if __name__ == "__main__":
    data = get_raw_data()
    logger.info(f"Extracted data: {data}")

