# HealthRAG Configuration
# All tunable settings live here — no magic numbers scattered around the codebase

import os
from dotenv import load_dotenv
load_dotenv()  # reads .env if present, silently skips if not

DATA_DIR = "data/processed"
MODELS_DIR = "models"

FAISS_INDEX_PATH = "data/processed/medquad.index"
EMBEDDINGS_PATH = "data/processed/embeddings.npy"
CHUNKS_META_PATH = "data/processed/chunks_meta.json"
CLASSIFIER_PATH = "models/symptom_classifier"
CATEGORIES_PATH = "data/processed/classifier/categories.json"

# played around with 256 and 1024, settled on 512
CHUNK_SIZE = 512  # words per chunk
OVERLAP = 50

TOP_K_RETRIEVAL = 5
RERANK_TOP_K = 5

# below this threshold the system adds a "consult a doctor" warning instead of answering
CONFIDENCE_THRESHOLD = 0.45

# set True to use Ollama (local Mistral) instead of OpenAI
USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
LOCAL_MODEL = "mistral"

MAX_CHAT_HISTORY = 4  # keep last 4 exchanges in memory

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8000

# Streamlit frontend
STREAMLIT_PORT = 8501
API_BASE_URL = "http://localhost:8000"
