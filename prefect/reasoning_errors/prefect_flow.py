import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="/usr/src/app/.env")

# Set up the Python path to include the common module
sys.path.append(os.getenv("PYTHONPATH"))

from prefect import flow, task
from datetime import datetime
import logging

# ...existing imports...
from src.pipelines.reasoning_errors.extract import get_raw_data
from src.pipelines.reasoning_errors.transform import transform_data
from src.pipelines.reasoning_errors.load import load_data_to_postgres

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@task
def extract():
    logger.info("Starting extraction")
    data = get_raw_data()
    return data

@task
def transform(raw_data):
    logger.info("Starting transformation")
    return transform_data(raw_data)

@task
def load(transformed_data):
    logger.info("Starting loading")
    if transformed_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        table_name = f"reasoning_errors_{timestamp}"
        load_data_to_postgres(transformed_data, table_name)
    else:
        logger.info("No data to load.")

@flow
def etl_flow():
    raw_data = extract()
    transformed = transform(raw_data)
    load(transformed)

if __name__ == "__main__":
    etl_flow()
