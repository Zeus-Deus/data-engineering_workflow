import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="/usr/src/app/.env")

# Set up the Python path to include the common module
sys.path.append(os.getenv("PYTHONPATH"))

from datetime import datetime
import logging
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.exc import SQLAlchemyError
from src.common.postgres_utils import get_postgres_engine
#from extract import get_raw_data
#from transform import transform_data
from src.pipelines.reasoning_errors.extract import get_raw_data
from src.pipelines.reasoning_errors.transform import transform_data

# Load environment variables
load_dotenv(dotenv_path="/usr/src/app/.env")

# Set up the Python path to include the common module
sys.path.append(os.getenv("PYTHONPATH"))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# PostgreSQL connection details
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB_REASONING_ERRORS")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

def create_table(engine, table_name):
    metadata = MetaData()
    table = Table(
        table_name, metadata,
        Column('id', Integer, primary_key=True),
        Column('bias_name', String),
        Column('h4_tag', String),
        Column('h3_tag', String),
        Column('h2_tag', String)
    )
    try:
        metadata.create_all(engine)
        logger.info(f"Successfully created table: {table_name}")
        return table
    except SQLAlchemyError as e:
        logger.error(f"Error creating table {table_name}: {e}")
        return None

def load_data_to_postgres(data, table_name):
    engine = get_postgres_engine(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB)
    if engine is None:
        logger.error("Failed to get PostgreSQL engine.")
        return

    table = create_table(engine, table_name)
    if table is None:
        logger.error("Failed to create table.")
        return

    try:
        with engine.connect() as connection:
            logger.info(f"Starting to load data into table: {table_name}")
            for row in data:
                connection.execute(table.insert().values(
                    bias_name=row['bias_name'],
                    h4_tag=row['h4_tag'],
                    h3_tag=row['h3_tag'],
                    h2_tag=row['h2_tag']
                ))
            connection.commit()
            logger.info(f"Successfully loaded data into table: {table_name}")
    except SQLAlchemyError as e:
        logger.error(f"Error loading data into table {table_name}: {e}")
    finally:
        connection.close()

def main():
    raw_data = get_raw_data()
    transformed_data = transform_data(raw_data)
    
    if transformed_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        table_name = f"reasoning_errors_{timestamp}"
        load_data_to_postgres(transformed_data, table_name)
    else:
        logger.info("No transformed data available to load.")

if __name__ == "__main__":
    main()