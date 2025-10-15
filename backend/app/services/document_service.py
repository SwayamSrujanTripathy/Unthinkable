import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from ..core.config import settings

# Langchain loaders are not directly used in this simplified version.
# We will read file content directly.
import PyPDF2
import io


# Initialize Sentence Transformer model
model = SentenceTransformer(settings.embedding_model)

# Initialize Pinecone
pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index(settings.PINECONE_INDEX_NAME)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text from a PDF file's bytes."""
    text = ""
    # PyPDF2 can raise exceptions for corrupted or encrypted files.
    try:
        with io.BytesIO(file_bytes) as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            if reader.is_encrypted:
                # Add handling for encrypted PDFs if necessary, for now, we'll skip them
                print(f"Skipping encrypted PDF file.")
                return ""
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    except PyPDF2.errors.PdfReadError as e:
        print(f"Could not read PDF. It might be corrupted or malformed. Error: {e}")
        return ""


def process_documents(files: List) -> bool:
    """
    Processes uploaded documents, splits them into chunks, creates embeddings,
    and upserts them into the Pinecone index.
    """
    try:
        all_chunks_text = []

        for file in files:
            content_bytes = file.file.read()
            text_content = ""
            if file.content_type == "application/pdf":
                text_content = extract_text_from_pdf(content_bytes)
            else: # Assuming plain text for others
                try:
                    text_content = content_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    print(f"Skipping file {file.filename} due to a decoding error. Please ensure it is UTF-8 encoded.")
                    continue

            if not text_content:
                print(f"No text content extracted from {file.filename}, skipping.")
                continue

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap
            )
            chunks = text_splitter.split_text(text_content)
            all_chunks_text.extend(chunks)

        if not all_chunks_text:
            print("No text was extracted from any of the provided documents.")
            return False

        # Create embeddings and prepare for upsert
        vectors_to_upsert = []
        # A unique prefix for this upload batch to avoid ID collisions
        upload_id = os.urandom(4).hex()
        for i, chunk_text in enumerate(all_chunks_text):
            embedding = model.encode(chunk_text).tolist()
            vector = {
                "id": f"doc_{upload_id}_chunk_{i}",
                "values": embedding,
                "metadata": {"text": chunk_text}
            }
            vectors_to_upsert.append(vector)

        # Upsert in batches
        batch_size = 100
        for i in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[i:i + batch_size]
            index.upsert(vectors=batch)

        print("Successfully processed and upserted documents.")
        return True

    except Exception as e:
        # This will catch other errors, like from Pinecone or SentenceTransformer
        print(f"An unexpected error occurred during document processing: {e}")
        return False

