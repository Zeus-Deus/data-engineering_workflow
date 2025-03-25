import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="/usr/src/app/.env")

# Set up the Python path to include the common module
sys.path.append(os.getenv("PYTHONPATH"))

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from src.common.database import MongoDBConnection

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MongoDB connection details
MONGO_DB = os.getenv("MONGO_DB_REASONING_ERRORS")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION_REASONING_ERRORS")

urls = [
    "https://en.wikipedia.org/wiki/List_of_cognitive_biases"
]

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        logger.info(f"Successfully fetched data from {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from {url}: {e}")
        return None

def parse_data(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        logger.info("Successfully parsed HTML content")
        return str(soup)
    except Exception as e:
        logger.error(f"Error parsing data: {e}")
        return None
    
def save_to_mongodb(url, html_content):
    try:
        db_connection = MongoDBConnection(db_name=MONGO_DB, collection_name=MONGO_COLLECTION)
        collection, client = db_connection.get_collection()
        
        # Check if document already exists to avoid duplicates
        existing_doc = collection.find_one({"url": url})
        if existing_doc:
            collection.update_one(
                {"url": url},
                {"$set": {"html_content": html_content}}
            )
            logger.info(f"Updated existing document for URL: {url}")
        else:
            document = {
                "url": url,
                "html_content": html_content,
                "timestamp": datetime.now()
            }
            collection.insert_one(document)
            logger.info(f"Inserted new document for URL: {url}")
    except Exception as e:
        logger.error(f"Error saving data to MongoDB: {e}")
    finally:
        client.close()

def main():
    logger.info("Starting data ingestion process")
    for url in urls:
        html_content = fetch_data(url)
        if html_content:
            parsed_content = parse_data(html_content)
            if parsed_content:
                save_to_mongodb(url, parsed_content)
    logger.info("Data ingestion process completed")

if __name__ == "__main__":
    main()