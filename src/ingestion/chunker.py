"""
chunker.py — splits a filing's text into LlamaIndex nodes.

Each node is a ~512-token chunk of text.
The metadata (ticker, company, form, date) is attached to every node
so Pinecone can filter by company or form type later.
"""

from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter


def filing_to_nodes(filing: dict, chunk_size: int = 512, chunk_overlap: int = 50):
    """
    Convert a filing dict (from fetcher.fetch_filing) into a list of TextNodes.

    chunk_size   — max tokens per chunk (512 ≈ a few paragraphs)
    chunk_overlap — tokens shared between adjacent chunks so context isn't lost
                    at a boundary
    """
    doc = Document(
        text=filing["text"],
        metadata={
            "ticker": filing["ticker"],
            "company": filing["company"],
            "form": filing["form"],
            "date": filing["date"],
        },
    )

    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    nodes = splitter.get_nodes_from_documents([doc])
    return nodes
