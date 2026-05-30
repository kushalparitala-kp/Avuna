"""
query.py — retrieves relevant chunks from Pinecone and answers questions via Groq.

Usage:
    from src.retrieval.query import query
    result = query("What was Apple's revenue in 2025?", tickers=["AAPL"])
    print(result["answer"])
    print(result["sources"])
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import config

from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.vector_stores.types import (
    MetadataFilters,
    MetadataFilter,
    FilterCondition,
)

Settings.llm = config.llm
Settings.embed_model = config.embed_model

INDEX_NAME = "avuna"


def _build_query_engine(tickers: list[str] | None, top_k: int):
    """Connect to Pinecone and return a query engine, optionally filtered by ticker."""
    pinecone_index = config.pc.Index(INDEX_NAME)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    index = VectorStoreIndex.from_vector_store(vector_store)

    if tickers:
        # Filter to only the requested companies (OR across tickers)
        filters = MetadataFilters(
            filters=[MetadataFilter(key="ticker", value=t) for t in tickers],
            condition=FilterCondition.OR,
        )
        return index.as_query_engine(
            llm=config.llm,
            similarity_top_k=top_k,
            filters=filters,
        )

    # No filter — search across all companies
    return index.as_query_engine(llm=config.llm, similarity_top_k=top_k)


def query(question: str, tickers: list[str] | None = None, top_k: int = 5) -> dict:
    """
    Answer a question using SEC filing data from Pinecone.

    Args:
        question — the natural language question to answer
        tickers  — list of ticker symbols to search (e.g. ["AAPL", "MSFT"]).
                   Pass None to search across all ingested companies.
        top_k    — number of chunks to retrieve from Pinecone (default 5)

    Returns a dict with:
        answer   — the LLM's answer as a string
        sources  — list of source chunks used, each with text + metadata
    """
    engine = _build_query_engine(tickers, top_k)
    response = engine.query(question)

    sources = [
        {
            "text": node.text[:300],  # first 300 chars of each source chunk
            "ticker": node.metadata.get("ticker"),
            "company": node.metadata.get("company"),
            "form": node.metadata.get("form"),
            "date": node.metadata.get("date"),
            "score": round(node.score, 3) if node.score else None,
        }
        for node in response.source_nodes
    ]

    return {
        "answer": str(response),
        "sources": sources,
    }
