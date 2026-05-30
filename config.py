"""
config.py — loads environment variables and initializes all external clients.

Import this module at the top of any file that needs:
    - the Pinecone client (pc)
    - the Groq LLM (llm)
    - the embedding model (embed_model)

edgartools is initialized here as a side effect (set_identity must run
before any edgar API call, so importing config.py is enough).
"""

import os
from dotenv import load_dotenv

# Load .env file into os.environ before reading any variables
load_dotenv()

# ── EDGAR ─────────────────────────────────────────────────────────────────────
# edgartools is installed as "edgartools" but imported as "edgar"
# set_identity sends your name+email as a User-Agent header to SEC EDGAR.
# This is required by SEC's terms of use — without it, requests will be blocked.
from edgar import set_identity

EDGAR_IDENTITY = os.environ["EDGAR_IDENTITY"]
set_identity(EDGAR_IDENTITY)

# ── PINECONE ──────────────────────────────────────────────────────────────────
from pinecone import Pinecone

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
pc = Pinecone(api_key=PINECONE_API_KEY)

# ── GROQ LLM (via LlamaIndex) ─────────────────────────────────────────────────
from llama_index.llms.groq import Groq

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
llm = Groq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

# ── EMBEDDING MODEL ───────────────────────────────────────────────────────────
# all-MiniLM-L6-v2 is a small, fast model that runs locally (no API needed).
# First run will download ~90 MB from HuggingFace; subsequent runs use the cache.
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
