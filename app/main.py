from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from app.ingest import process_pdf
from app.query import ask_question
import os
import shutil

app = FastAPI(title="RAG Assistant API")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.get("/")
def home():
    return {"message": "RAG Assistant API is running"}

@app.post("/upload")
async def upload_and_ingest(file: UploadFile = File(...)):
    """Upload a file and immediately ingest it."""
    try:
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        result = process_pdf(file_path)
        return {"message": f"Successfully uploaded and {result}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
def ingest_document():
    """Endpoint to ingest the default sample PDF."""
    try:
        file_path = "uploads/sample.pdf"
        if not os.path.exists(file_path):
            raise FileNotFoundError("Default sample.pdf not found.")
        result = process_pdf(file_path)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_assistant(request: QueryRequest):
    """Endpoint to ask a question based on ingested documents."""
    try:
        answer = await ask_question(request.question)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
