"""
bulk_ingest.py — ingests the latest 10-K for all companies except AAPL.

Reuses:
    fetch_filing()   from src.ingestion.fetcher
    filing_to_nodes() from src.ingestion.chunker
    ingest_nodes()   from src.ingestion.indexer

Run:
    source venv/bin/activate
    python -m src.ingestion.bulk_ingest
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.ingestion.fetcher import fetch_filing, COMPANIES
from src.ingestion.chunker import filing_to_nodes
from src.ingestion.indexer import ingest_nodes

# AAPL already ingested — skip it
TICKERS = [t for t in COMPANIES if t != "AAPL"]

results = []

print(f"Bulk ingesting 10-K for {len(TICKERS)} companies: {', '.join(TICKERS)}\n")

for ticker in TICKERS:
    company = COMPANIES[ticker]
    print(f"[{ticker}] {company} — fetching 10-K...")
    t0 = time.time()

    try:
        filing = fetch_filing(ticker, form="10-K")
        nodes = filing_to_nodes(filing)
        count = ingest_nodes(nodes)
        elapsed = time.time() - t0

        print(f"[{ticker}] Done — {count} vectors stored in {elapsed:.1f}s\n")
        results.append({"ticker": ticker, "company": company, "vectors": count, "time": elapsed, "status": "ok"})

    except Exception as e:
        elapsed = time.time() - t0
        print(f"[{ticker}] FAILED after {elapsed:.1f}s — {e}\n")
        results.append({"ticker": ticker, "company": company, "vectors": 0, "time": elapsed, "status": f"error: {e}"})

# ── Summary ───────────────────────────────────────────────────────────────────
print("=" * 60)
print(f"{'Ticker':<8} {'Company':<16} {'Vectors':>8} {'Time':>7}  Status")
print("─" * 60)
for r in results:
    print(f"{r['ticker']:<8} {r['company']:<16} {r['vectors']:>8} {r['time']:>6.1f}s  {r['status']}")

total_vectors = sum(r["vectors"] for r in results)
total_time = sum(r["time"] for r in results)
failures = [r for r in results if r["status"] != "ok"]

print("─" * 60)
print(f"{'TOTAL':<8} {'':<16} {total_vectors:>8} {total_time:>6.1f}s")
print(f"\n{len(results) - len(failures)}/{len(results)} succeeded.")
if failures:
    print(f"Failed: {', '.join(r['ticker'] for r in failures)}")
print("=" * 60)
