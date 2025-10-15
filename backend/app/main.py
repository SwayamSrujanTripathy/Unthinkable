from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from pydantic import BaseModel

from .services import document_service, rag_service

app = FastAPI(
    title="RAG System API",
    description="API for document ingestion and question answering using RAG.",
    version="1.0.0"
)

# Initialize the RAG service
rag_pipeline = rag_service.RAGService()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    context: List[str]

@app.post("/upload-documents/", status_code=201)
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload and process multiple documents.
    """
    all_chunks = []
    for file in files:
        if file.content_type == "application/pdf":
            text = document_service.extract_text_from_pdf(file.file)
        elif file.content_type == "text/plain":
            text = document_service.extract_text_from_txt(file.file)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")
        
        chunks = document_service.get_text_chunks(text)
        all_chunks.extend(chunks)

    if all_chunks:
        rag_pipeline.store_embeddings(all_chunks)

    return {"message": f"Successfully processed and indexed {len(files)} documents."}


@app.post("/query/", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Endpoint to process a user query and get an answer.
    """
    try:
        context = rag_pipeline.retrieve_relevant_chunks(request.query)
        if not context:
            return QueryResponse(answer="I couldn't find any relevant information in the documents.", context=[])
            
        answer = rag_pipeline.generate_answer(request.query, context)
        return QueryResponse(answer=answer, context=context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG API"}
