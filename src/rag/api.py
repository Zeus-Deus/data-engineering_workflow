import os
import sys
from dotenv import load_dotenv
import logging

# Load environment variables early
load_dotenv(dotenv_path="/usr/src/app/.env")

sys.path.append(os.getenv("PYTHONPATH"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.rag.rag_qa import answer_question

app = FastAPI()

# Add CORS middleware to allow requests from the chat-ui
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "RAG API is running"}

@app.post("/query")
async def query_rag(request: QueryRequest):
    try:
        answer = answer_question(request.question)
        logging.info(f"API Response: {answer}")
        
        # Return a simple JSON response
        return {
            "answer": answer
        }
    except Exception as e:
        logging.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))