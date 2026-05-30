"""
indexer.py — embeds nodes and upserts them into Pinecone.

Creates the Pinecone index on first run (dimension=384 for all-MiniLM-L6-v2).
Subsequent runs reuse the existing index.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import config

from pinecone import ServerlessSpec
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext

# Tell LlamaIndex which LLM and embedding model to use globally
Settings.llm = config.llm
Settings.embed_model = config.embed_model

INDEX_NAME = "avuna"
DIMENSION = 384  # all-MiniLM-L6-v2 produces 384-dimensional vectors


def get_or_create_index():
    """Returns the Pinecone Index object, creating it first if needed."""
    existing = [i.name for i in config.pc.list_indexes()]

    if INDEX_NAME not in existing:
        print(f"Creating Pinecone index '{INDEX_NAME}' (dimension={DIMENSION}, metric=cosine)...")
        config.pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        print("Index created.")
    else:
        print(f"Using existing Pinecone index '{INDEX_NAME}'.")

    return config.pc.Index(INDEX_NAME)


def ingest_nodes(nodes: list) -> int:
    """
    Embed a list of TextNodes and upsert them into Pinecone.
    Returns the number of nodes ingested.
    """
    pinecone_index = get_or_create_index()
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    VectorStoreIndex(nodes, storage_context=storage_context, show_progress=True)

    return len(nodes)
