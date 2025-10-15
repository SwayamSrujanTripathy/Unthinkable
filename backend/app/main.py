from fastapi import FastAPI, UploadFile, HTTPException, File
from typing import List
from pydantic import BaseModel
from .services import document_service, rag_service

app = FastAPI(title="RAG System API")

class Query(BaseModel):
    text: str

@app.post("/upload-documents/")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload and process multiple documents (PDFs or TXTs).
    """
    # The document_service module has a process_documents function
    success = document_service.process_documents(files)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to process documents.")
    return {"message": "Documents processed and indexed successfully."}

@app.post("/query/")
async def query_system(query: Query):
    """
    Endpoint to ask a question and get a synthesized answer from the RAG system.
    """
    # The rag_service module has a query_rag function, which we call directly
    answer = rag_service.query_rag(query.text)
    if not answer:
        raise HTTPException(status_code=404, detail="Could not generate an answer.")
    return {"answer": answer}

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG API. Use the /docs endpoint to see the API documentation."}

