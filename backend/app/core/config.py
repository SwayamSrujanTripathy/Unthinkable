import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from a .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Configuration settings for the application.
    Reads environment variables and provides them to the application.
    """
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "rag-index")
    embedding_model: str = "all-MiniLM-L6-v2"
    generative_model: str = "models/gemini-2.5-flash"
    top_k: int = 3
    chunk_size: int = 1000
    chunk_overlap: int = 100

    class Config:
        case_sensitive = True
        env_file = ".env"

def get_settings() -> Settings:
    """Returns the settings instance."""
    return Settings()

settings = get_settings()
