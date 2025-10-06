"""
Configuration file for the Document Chatbot
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
VECTOR_DB_DIR = DATA_DIR / "vector_db"

# Create directories if they don't exist
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o"  # or "gpt-4-turbo", "gpt-3.5-turbo"

# Embedding Configuration
CHUNK_SIZE = 1000  # characters per chunk
CHUNK_OVERLAP = 200  # overlap between chunks

# Retrieval Configuration
TOP_K_RESULTS = 10  # number of relevant chunks to retrieve (increased for more context)

# Vector Store Configuration
VECTOR_STORE_TYPE = "faiss"  # Options: "faiss" or "chroma"
COLLECTION_NAME = "documents"

# Supported file types
SUPPORTED_EXTENSIONS = [".pdf", ".doc", ".docx", ".txt"]

# Error messages
ERROR_NO_CONTEXT = "⚠️ I couldn't find that information in your documents."
ERROR_NO_API_KEY = "⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your .env file."
