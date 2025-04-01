import os
from azure.storage.blob import BlobServiceClient
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_blob_content(blob_name, container_name=None, connection_string=None):
    connection_string = connection_string or os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = container_name or os.getenv("AZURE_BLOB_CONTAINER")
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        download_stream = blob_client.download_blob()
        content = download_stream.readall().decode('utf-8')
        logger.info(f"Successfully fetched blob '{blob_name}' from container '{container_name}'")
        return content
    except Exception as e:
        logger.error(f"Error fetching blob '{blob_name}': {e}")
        return None

def upload_blob_content(blob_name, data, container_name=None, connection_string=None):
    """
    Uploads data to a blob (creates or overwrites the blob).
    """
    connection_string = connection_string or os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = container_name or os.getenv("AZURE_BLOB_CONTAINER")
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        # Ensure the container exists
        try:
            container_client.get_container_properties()
        except Exception:
            container_client.create_container()
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)
        logger.info(f"Successfully uploaded blob '{blob_name}' to container '{container_name}'")
        return True
    except Exception as e:
        logger.error(f"Error uploading blob '{blob_name}': {e}")
        return False