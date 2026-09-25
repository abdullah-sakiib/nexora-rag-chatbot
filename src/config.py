import os
from dotenv import load_dotenv

load_dotenv()

PDF_DIR = "data/pdfs"
VECTORSTORE_DIR = "vectorstore"
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Database password: IamSakib123