import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env and set up Python path
load_dotenv(dotenv_path="/usr/src/app/.env")
sys.path.append(os.getenv("PYTHONPATH"))

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from src.common.azure_blob_storage import upload_blob_content

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# List of URLs to ingest raw data from
urls = [
    "https://en.wikipedia.org/wiki/List_of_cognitive_biases"
]

def fetch_data(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for HTTP errors
        logger.info(f"Successfully fetched data from {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from {url}: {e}")
        return ""

def parse_data(html_content: str) -> str:
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        logger.info("Successfully parsed HTML content")
        return str(soup)
    except Exception as e:
        logger.error(f"Error parsing data: {e}")
        return ""

def upload_raw_data(url: str, html_content: str) -> None:
    try:
        # Create a unique blob name using a timestamp,
        # you might also incorporate parts of the URL for clarity.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        blob_name = f"raw_data_{timestamp}.html"
        if upload_blob_content(blob_name, html_content):
            logger.info(f"Uploaded raw data for URL '{url}' to blob '{blob_name}'")
        else:
            logger.error(f"Failed to upload raw data for URL: {url}")
    except Exception as e:
        logger.error(f"Error uploading raw data for URL '{url}': {e}")

def main() -> None:
    logger.info("Starting Azure Data Ingestion Process")
    for url in urls:
        html_content = fetch_data(url)
        if html_content:
            parsed_content = parse_data(html_content)
            if parsed_content:
                upload_raw_data(url, parsed_content)
    logger.info("Azure Data Ingestion Process Completed")

if __name__ == "__main__":
    main()