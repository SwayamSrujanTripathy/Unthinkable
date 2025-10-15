import os
from typing import List, Dict

import google.generativeai as genai
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

from backend.app.core.config import settings

# Configure the Gemini API
genai.configure(api_key=settings.GOOGLE_API_KEY)

class RAGService:
    """
    Service for handling the entire RAG pipeline.
    """
    def __init__(self):
        self.pinecone = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.index_name = settings.PINECONE_INDEX_NAME
        self.llm = genai.GenerativeModel('gemini-pro')
        self._create_pinecone_index_if_not_exists()

    def _create_pinecone_index_if_not_exists(self):
        """
        Creates a Pinecone index if it doesn't already exist.
        """
        if self.index_name not in self.pinecone.list_indexes().names():
            self.pinecone.create_index(
                name=self.index_name,
                dimension=self.embedding_model.get_sentence_embedding_dimension(),
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
        self.index = self.pinecone.Index(self.index_name)

    def store_embeddings(self, chunks: List[str]):
        """
        Generates embeddings for text chunks and stores them in Pinecone.
        """
        embeddings = self.embedding_model.encode(chunks, convert_to_tensor=False)
        vectors_to_upsert = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector_id = f"doc_chunk_{i}"
            metadata = {"text": chunk}
            vectors_to_upsert.append((vector_id, embedding.tolist(), metadata))
        
        self.index.upsert(vectors=vectors_to_upsert)

    def retrieve_relevant_chunks(self, query: str, top_k: int = 5) -> List[str]:
        """
        Retrieves the most relevant text chunks for a given query.
        """
        query_embedding = self.embedding_model.encode([query], convert_to_tensor=False)[0].tolist()
        results = self.index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
        
        return [match['metadata']['text'] for match in results['matches']]

    def get_conversational_chain(self):
        """
        Creates a prompt template and returns a conversational chain.
        """
        prompt_template = """
        Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
        provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
        """
        return prompt_template

    def generate_answer(self, query: str, context: List[str]) -> str:
        """
        Generates an answer using the LLM based on the query and context.
        """
        prompt_template = self.get_conversational_chain()
        prompt = prompt_template.format(context="\n".join(context), question=query)
        
        response = self.llm.generate_content(prompt)
        return response.text

rag_service = RAGService()
