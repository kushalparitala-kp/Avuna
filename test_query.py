"""
test_query.py — tests the retrieval pipeline against Apple's 10-K.

Run:
    source venv/bin/activate
    python test_query.py
"""

from src.retrieval.query import query

QUESTIONS = [
    {
        "q": "What was Apple's total net sales for fiscal year 2025?",
        "tickers": ["AAPL"],
        "label": "Factual / financial number",
    },
    {
        "q": "What are the main risk factors Apple faces?",
        "tickers": ["AAPL"],
        "label": "Qualitative / risk analysis",
    },
    {
        "q": "What products and services does Apple sell?",
        "tickers": None,  # no filter — searches all ingested data
        "label": "No filter (cross-company ready)",
    },
]


for i, item in enumerate(QUESTIONS, 1):
    print(f"\n{'=' * 60}")
    print(f"Question {i} [{item['label']}]")
    print(f"Q: {item['q']}")
    if item["tickers"]:
        print(f"Filter: {item['tickers']}")
    else:
        print("Filter: none (all companies)")
    print("─" * 60)

    result = query(item["q"], tickers=item["tickers"])

    print(f"Answer:\n{result['answer']}")
    print(f"\nSources used ({len(result['sources'])}):")
    for s in result["sources"]:
        print(f"  [{s['ticker']} {s['form']} {s['date']} | score={s['score']}]")
        print(f"  '{s['text'][:120]}...'")

print(f"\n{'=' * 60}")
print("All queries complete.")
