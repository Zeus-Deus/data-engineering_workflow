import os
import logging
import requests  # <-- added to fetch remote content
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv(dotenv_path="/usr/src/app/.env")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Qdrant connection parameters (add these variables to your .env if not present)
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE"))  # Adjust based on your chosen model
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION")

# Initialize Qdrant client
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def create_collection(force_recreate: bool = False):
    """
    Creates the Qdrant collection if it doesn't exist.
    If it exists and the vector dimensions don't match the expected VECTOR_SIZE,
    the collection is recreated if force_recreate is True.
    """
    try:
        existing_collections = [col.name for col in client.get_collections().collections]
        if COLLECTION_NAME in existing_collections:
            collection_info = client.get_collection(collection_name=COLLECTION_NAME)
            # Access the vector size from the collection config
            current_dim = collection_info.config.params.vectors.size
            if current_dim != VECTOR_SIZE:
                msg = (f"Existing Qdrant collection is configured for dense vectors with {current_dim} dimensions. "
                       f"Selected embeddings are {VECTOR_SIZE}-dimensional.")
                if force_recreate:
                    client.recreate_collection(
                        collection_name=COLLECTION_NAME,
                        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
                    )
                    logger.info(f"Recreated Qdrant collection '{COLLECTION_NAME}' with force_recreate=True")
                else:
                    raise ValueError(msg + " If you want to recreate the collection, set force_recreate=True")
            else:
                logger.info(f"Qdrant collection '{COLLECTION_NAME}' already exists with correct dimensions.")
        else:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
            )
            logger.info(f"Created Qdrant collection '{COLLECTION_NAME}'")
    except Exception as e:
        logger.error(f"Error creating collection: {e}")
        raise

def vectorize_text(text: str) -> list:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    vector = model.encode(text).tolist()
    logger.info(f"Generated vector of length {len(vector)} for text: {text[:100]}...")
    return vector

def upsert_vector(text: str, point_id: int):
    vector = vectorize_text(text)
    point = PointStruct(
        id=point_id,
        vector=vector,
        payload={"text": text}
    )
    try:
        logger.info(f"Attempting to upsert point_id {point_id} into collection '{COLLECTION_NAME}'")
        response = client.upsert(collection_name=COLLECTION_NAME, points=[point])
        logger.info(f"Upsert response: {response}")
        logger.info(f"Successfully upserted point_id {point_id} with vector length {len(vector)}")
    except Exception as e:
        logger.error(f"Error upserting vector: {e}")

if __name__ == "__main__":
    create_collection()
    # List of URLs to ingest raw data from
    urls = [
        "https://en.wikipedia.org/wiki/List_of_cognitive_biases"
    ]
    
    point_id = 1
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            wiki_content = response.text
            upsert_vector(wiki_content, point_id=point_id)
            logger.info(f"Vectorization and upsert completed for URL: {url}")
            point_id += 1
        except Exception as e:
            logger.error(f"Error processing URL {url}: {e}")