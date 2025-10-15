import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from ..core.config import settings

# Configure the generative AI model
genai.configure(api_key=settings.GOOGLE_API_KEY)
model = SentenceTransformer(settings.embedding_model)
genai_model = genai.GenerativeModel(settings.generative_model)

# Initialize Pinecone
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

def get_or_create_index():
    """Gets an existing Pinecone index or creates a new one if it doesn't exist."""
    if settings.PINECONE_INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=settings.PINECONE_INDEX_NAME,
            dimension=model.get_sentence_embedding_dimension(),
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
    return pc.Index(settings.PINECONE_INDEX_NAME)

index = get_or_create_index()

def query_rag(query_text: str) -> str:
    """
    Queries the RAG system to get an answer for a given text.
    1. Encodes the query to get a vector embedding.
    2. Queries Pinecone to find the most relevant document chunks.
    3. Constructs a prompt with the context and query.
    4. Calls the Gemini model to get a synthesized answer.
    """
    try:
        # 1. Encode the query
        query_embedding = model.encode(query_text).tolist()

        # 2. Query Pinecone
        query_results = index.query(
            vector=query_embedding,
            top_k=settings.top_k,
            include_metadata=True
        )

        # 3. Construct the prompt
        context = " ".join([match['metadata']['text'] for match in query_results['matches']])
        prompt = f"""
        Use the following context to answer the question.
        If you don't know the answer, just say that you don't know.
        
        Context:
        {context}
        
        Question:
        {query_text}
        
        Answer:
        """

        # 4. Get the answer from Gemini
        response = genai_model.generate_content(prompt)
        
        return response.text

    except Exception as e:
        print(f"An error occurred during the RAG query: {e}")
        return "Sorry, I encountered an error while processing your request."

