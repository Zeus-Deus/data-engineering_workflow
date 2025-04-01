import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="/usr/src/app/.env")

# Set up the Python path to include the common module
sys.path.append(os.getenv("PYTHONPATH"))

from prefect import flow, task
import logging
from src.data_ingestion.reasoning_errors_to_mongodb import urls, fetch_data, parse_data, save_to_mongodb
from src.data_ingestion.reasoning_errors_to_azure import upload_raw_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@task
def process_url(url: str):
    try:
        logger.info(f"Fetching data from {url}")
        html_content = fetch_data(url)
        if not html_content:
            logger.error(f"No data fetched from {url}")
            return
        parsed_content = parse_data(html_content)
        if not parsed_content:
            logger.error(f"Failed to parse data from {url}")
            return

        # Check if we are using Azure Blob Storage or MongoDB
        use_azure = os.getenv("USE_AZURE", "False").lower() in ("true", "1")
        if use_azure:
            logger.info("Uploading data to Azure Blob Storage")
            upload_raw_data(url, parsed_content)
        else:
            logger.info("Saving data to MongoDB")
            save_to_mongodb(url, parsed_content)

        logger.info(f"Data ingestion successful for {url}")
    except Exception as e:
        logger.error(f"Error processing URL {url}: {e}")

@flow
def data_ingestion_flow():
    for url in urls:
        process_url.submit(url)

if __name__ == "__main__":
    data_ingestion_flow()
