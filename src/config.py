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

# AI Provider Selection
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")  # Options: "openai", "gemini"

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o"  # or "gpt-4-turbo", "gpt-3.5-turbo"

# Google Gemini Configuration (FREE!)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_CHAT_MODEL = "gemini-1.5-flash"  # Fast and FREE! or "gemini-1.5-pro"
GEMINI_EMBED_MODEL = "models/embedding-001"

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
ERROR_NO_API_KEY = "⚠️ API key not found. Please set GOOGLE_API_KEY or OPENAI_API_KEY in your .env file."

# Get active API key based on provider
def get_active_api_key():
    """Get the API key for the selected provider"""
    if AI_PROVIDER == "gemini":
        return GOOGLE_API_KEY
    else:
        return OPENAI_API_KEY

ACTIVE_API_KEY = get_active_api_key()
