import os
import sys
from dotenv import load_dotenv
import logging

# Load environment variables early
load_dotenv(dotenv_path="/usr/src/app/.env")

sys.path.append(os.getenv("PYTHONPATH"))

# Import necessary classes from updated packages
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# Import create_collection from the vectorization module
from src.vectorization.vectorize import create_collection

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def create_qa_chain() -> RetrievalQA:
    """
    Create and return a RetrievalQA chain that uses Qdrant as a vector store and
    the OpenAI LLM for question answering.
    """
    try:
        # Retrieve necessary environment variables
        qdrant_host = os.getenv("QDRANT_HOST")
        qdrant_port = int(os.getenv("QDRANT_PORT"))
        collection_name = os.getenv("QDRANT_COLLECTION")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not set in .env file.")
        
        # Initialize the embeddings provider using OpenAI
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        
        # Initialize QdrantClient with host and port
        client = QdrantClient(
            url=f"http://{qdrant_host}:{qdrant_port}"
        )
        
        # Ensure the Qdrant collection exists with the correct dimensions.
        # Set force_recreate=True if you want to update the collection if dimensions differ.
        create_collection(force_recreate=True)
        
        # Initialize QdrantVectorStore
        vectorstore = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embeddings
        )
        
        # Initialize the OpenAI LLM (e.g., GPT-4)
        llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)
        
        # Create the retrieval-based QA chain using the 'stuff' chain type.
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
        )
        
        logger.info("QA chain successfully created.")
        return qa_chain
    except Exception as e:
        logger.error(f"Failed to create QA chain: {e}")
        raise

def answer_question(question: str) -> str:
    """
    Given a user question, use the QA chain to retrieve relevant information
    and generate an answer.
    """
    try:
        qa_chain = create_qa_chain()
        answer = qa_chain.run(question)
        logger.info(f"Raw answer from QA chain: {answer}")
        if not isinstance(answer, str):
            logger.error(f"Answer is not a string, it's a {type(answer)}")
            answer = str(answer)
        logger.info("Question answered successfully.")
        return answer
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        return "Error processing the question."

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ask a question using the RAG system.")
    parser.add_argument("question", type=str, help="The question to ask.")
    args = parser.parse_args()

    result = answer_question(args.question)
    print("Answer:", result)
