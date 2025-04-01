import sys
import os
from dotenv import load_dotenv

# Load environment variables early
load_dotenv("/usr/src/app/.env")

# Add the PYTHONPATH to sys.path
sys.path.append(os.getenv("PYTHONPATH", "."))

from prefect import flow, task
import requests
import logging
from bs4 import BeautifulSoup

# Import the functions from your vectorization module
from src.vectorization.vectorize import create_collection, upsert_vector

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# List of URLs to process for vectorization
URLS = [
    "https://en.wikipedia.org/wiki/List_of_cognitive_biases"
]

@task
def create_qdrant_collection():
    try:
        logger.info(f"Connecting to Qdrant at {os.getenv('QDRANT_HOST')}:{os.getenv('QDRANT_PORT')}")
        create_collection()
        logger.info("Qdrant collection creation completed.")
    except Exception as e:
        logger.error(f"Error creating collection: {e}")
        raise

@task
def fetch_url_content(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info(f"Fetched content from {url}")
        return response.text
    except Exception as e:
        logger.error(f"Error fetching content from {url}: {e}")
        raise

@task
def vectorize_and_upsert(html_content: str, point_id: int):
    try:
        # Clean the HTML content to extract plain text
        soup = BeautifulSoup(html_content, 'html.parser')
        plain_text = soup.get_text(separator=" ", strip=True)  # Extract plain text

        # Log the cleaned text for debugging (optional)
        logger.info(f"Cleaned text for point_id {point_id}: {plain_text[:100]}...")  # Log first 100 chars

        # Vectorize and upsert the cleaned text
        upsert_vector(plain_text, point_id)
        logger.info(f"Processed vector for point_id {point_id}")
    except Exception as e:
        logger.error(f"Error upserting vector for point_id {point_id}: {e}")
        raise

@flow
def vectorization_flow():
    # Ensure the Qdrant collection exists
    create_qdrant_collection()

    point_id = 1
    for url in URLS:
        # Fetch and vectorize each URL sequentially.
        text = fetch_url_content(url)
        vectorize_and_upsert(text, point_id)
        point_id += 1

if __name__ == "__main__":
    vectorization_flow()