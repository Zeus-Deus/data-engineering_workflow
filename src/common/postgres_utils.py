import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_postgres_engine(user, password, host, port, db_name):
    try:
        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}")
        return engine
    except SQLAlchemyError as e:
        logging.error(f"Error connecting to PostgreSQL: {e}")
        return None
