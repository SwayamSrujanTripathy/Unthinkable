# RAG System with FastAPI, Streamlit, Pinecone, and Gemini

This project implements a Retrieval-Augmented Generation (RAG) system to answer questions based on a collection of uploaded documents.

## Architecture

The system consists of three main components:

1.  **Backend (FastAPI):** An API to handle document uploads, processing, and user queries.
2.  **Frontend (Streamlit):** A user-friendly web interface for uploading documents and asking questions.
3.  **RAG Pipeline:** The core logic that processes documents, stores them in a vector database (Pinecone), retrieves relevant information, and generates answers using an LLM (Gemini).

### How it Works

1.  **Document Upload:** Users upload text or PDF documents through the Streamlit frontend.
2.  **Processing & Embedding:** The FastAPI backend processes the documents by:
    * Extracting text.
    * Splitting the text into smaller, manageable chunks.
    * Generating vector embeddings for each chunk using a sentence-transformer model.
    * Storing these embeddings in a Pinecone vector database.
3.  **Querying:**
    * A user submits a query through the frontend.
    * The backend generates an embedding for the query.
    * It uses this embedding to search Pinecone for the most similar (relevant) document chunks.
    * The retrieved chunks and the original query are passed to the Gemini LLM.
4.  **Answer Synthesis:** The Gemini model synthesizes a comprehensive answer based on the provided context from the documents and sends it back to the user.

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI application setup and endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── document_service.py # Logic for PDF/text processing
│   │   │   └── rag_service.py      # Core RAG logic (embedding, retrieval, synthesis)
│   │   └── core/
│   │       ├── __init__.py
│   │       └── config.py           # Configuration management (API keys)
│   └── Dockerfile
├── frontend/
│   ├── app.py              # Streamlit frontend application
│   └── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Setup and Installation

### Prerequisites

* Python 3.8+
* Docker and Docker Compose
* API Keys for:
    * Pinecone
    * Google (for Gemini)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create a `.env` file** in the `backend/app/core` directory and add your API keys:
    ```env
    GOOGLE_API_KEY="your_google_api_key"
    PINECONE_API_KEY="your_pinecone_api_key"
    PINECONE_ENVIRONMENT="your_pinecone_environment"
    PINECONE_INDEX_NAME="your_pinecone_index_name"
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application using Docker Compose:**
    ```bash
    docker-compose up --build
    ```

    This will start both the FastAPI backend and the Streamlit frontend.

    * **Backend API:** Available at `http://localhost:8000/docs`
    * **Frontend UI:** Available at `http://localhost:8501`

## Usage

1.  Open your browser and navigate to `http://localhost:8501`.
2.  Use the sidebar to upload your text or PDF documents.
3.  Once the documents are processed and indexed, you can ask questions in the main text area.
4.  The system will retrieve relevant information from your documents and generate an answer.
