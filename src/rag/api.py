import os
import sys
from dotenv import load_dotenv
import logging

# Load environment variables early
load_dotenv(dotenv_path="/usr/src/app/.env")

sys.path.append(os.getenv("PYTHONPATH"))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.rag.rag_qa import answer_question

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_rag(request: QueryRequest):
    try:
        answer = answer_question(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))