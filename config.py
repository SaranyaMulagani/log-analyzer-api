import os
from dotenv import load_dotenv

load_dotenv()

# Groq API (Free)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")
GROQ_MODEL   = os.getenv("GROQ_MODEL", "llama3-8b-8192")

# ChromaDB
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

# Chunking
CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))