import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_postgres_engine():
    # Flag to select which connection to use
    use_azure_pg = os.getenv("USE_AZURE_PG", "False").lower() in ("true", "1")
    
    if use_azure_pg:
        user = os.getenv("AZURE_POSTGRES_USER")
        password = os.getenv("AZURE_POSTGRES_PASSWORD")
        host = os.getenv("AZURE_POSTGRES_HOST")
        port = os.getenv("AZURE_POSTGRES_PORT")
        db_name = os.getenv("AZURE_POSTGRES_DB_REASONING_ERRORS")
        # Append SSL parameters if required by Azure
        connection_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}?sslmode=require"
    else:
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT")
        db_name = os.getenv("POSTGRES_DB_REASONING_ERRORS")
        connection_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    
    try:
        engine = create_engine(connection_url)
        logging.info(f"Connected to PostgreSQL at {host}:{port} using database {db_name}")
        return engine
    except SQLAlchemyError as e:
        logging.error(f"Error connecting to PostgreSQL: {e}")
        return None
