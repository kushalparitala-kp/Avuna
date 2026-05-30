"""
test_fetch.py — fetches Apple's latest 10-K and prints stats.

Run:
    source venv/bin/activate
    python test_fetch.py

This does NOT chunk or embed anything yet — we just want to see
what the raw text looks like before building the rest of the pipeline.
"""

from src.ingestion.fetcher import fetch_filing

print("Fetching Apple 10-K from SEC EDGAR...")
print("(This may take 10-30 seconds on first run)\n")

result = fetch_filing("AAPL", form="10-K")

text = result["text"]
words = len(text.split())
chars = len(text)

print(f"Company  : {result['company']} ({result['ticker']})")
print(f"Form     : {result['form']}")
print(f"Filed    : {result['date']}")
print(f"Size     : {chars:,} characters / {words:,} words")
print(f"Est. pages: ~{words // 400}")  # average 400 words per page
print()
print("─" * 60)
print("FIRST 1000 CHARACTERS:")
print("─" * 60)
print(text[:1000])
print()
print("─" * 60)
print("LAST 500 CHARACTERS:")
print("─" * 60)
print(text[-500:])
