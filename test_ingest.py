"""
test_ingest.py — runs the full ingestion pipeline for Apple's 10-K.

Steps:
  1. Fetch the latest AAPL 10-K from SEC EDGAR
  2. Chunk it into ~512-token nodes
  3. Embed each node with all-MiniLM-L6-v2
  4. Upsert into Pinecone

Run:
    source venv/bin/activate
    python test_ingest.py
"""

import time
from src.ingestion.fetcher import fetch_filing
from src.ingestion.chunker import filing_to_nodes
from src.ingestion.indexer import ingest_nodes

# ── Step 1: Fetch ─────────────────────────────────────────────────────────────
print("Step 1/3 — Fetching Apple 10-K from SEC EDGAR...")
t0 = time.time()
filing = fetch_filing("AAPL", form="10-K")
print(f"  Fetched: {filing['company']} {filing['form']} filed {filing['date']}")
print(f"  Text size: {len(filing['text']):,} chars ({len(filing['text'].split()):,} words)")
print(f"  Time: {time.time() - t0:.1f}s\n")

# ── Step 2: Chunk ─────────────────────────────────────────────────────────────
print("Step 2/3 — Splitting into chunks...")
t1 = time.time()
nodes = filing_to_nodes(filing)
print(f"  Created {len(nodes)} chunks")
print(f"  Sample chunk (first 200 chars):")
print(f"    '{nodes[0].text[:200]}...'")
print(f"  Metadata on each chunk: {nodes[0].metadata}")
print(f"  Time: {time.time() - t1:.1f}s\n")

# ── Step 3: Embed + store ─────────────────────────────────────────────────────
print("Step 3/3 — Embedding and uploading to Pinecone...")
print("  (First run downloads the embedding model ~90 MB — subsequent runs are fast)")
t2 = time.time()
count = ingest_nodes(nodes)
print(f"\n  Ingested {count} vectors")
print(f"  Time: {time.time() - t2:.1f}s\n")

# ── Summary ───────────────────────────────────────────────────────────────────
total = time.time() - t0
print("=" * 50)
print(f"Done. {count} vectors in Pinecone.")
print(f"Total time: {total:.1f}s")
print("=" * 50)
