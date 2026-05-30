# Avuna

> Institutional-grade financial intelligence. Open source.

Avuna is a RAG (Retrieval-Augmented Generation) system that lets you ask natural language questions across SEC filings from the top S&P 500 companies — and get answers grounded in the actual source documents.

---

## The Problem

Hedge funds and institutional investors use tools like Bloomberg Terminal ($24,000/year) to query financial filings at scale. Everyone else reads PDFs manually.

Avuna closes that gap. Built entirely on free, public SEC EDGAR data — the same filings Wall Street uses — and open source.

---

## What You Can Ask

- *"What did Apple say about iPhone demand in their last 10-K?"*
- *"Which companies flagged rising labor costs as a risk factor this quarter?"*
- *"How has Microsoft described its AI investment strategy across the last 4 filings?"*
- *"Which companies mentioned macro uncertainty but reported revenue growth?"*

---

## How It Works

SEC EDGAR API → Document Chunking → Embeddings → Pinecone
↓
User Query → Retrieval → Groq LLM → Grounded Answer

1. **Ingest** — Pull 10-K filings directly from SEC EDGAR via edgartools
2. **Chunk** — Split documents into semantically meaningful segments
3. **Embed** — Convert chunks to vector embeddings (all-MiniLM-L6-v2)
4. **Retrieve** — Find the most relevant chunks for any query
5. **Generate** — Groq LLM produces an answer grounded in retrieved context

---

## Data

All data sourced directly from SEC EDGAR — free, public, and legally accessible. No scraping. No paywalls.

**Coverage:** Top 10 S&P 500 companies by market cap
**Companies:** Apple, Microsoft, NVIDIA, Amazon, Alphabet, Meta, Tesla, Broadcom, JPMorgan, UnitedHealth
**Filing types:** 10-K (annual)

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Data | SEC EDGAR via edgartools |
| Vector DB | Pinecone serverless |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Orchestration | LlamaIndex |
| LLM | Groq (llama-3.3-70b-versatile) |
| UI | Streamlit |
| Language | Python |

---

## Project Status

✅ Ingestion pipeline — all 10 companies, 1,684 vectors in Pinecone
✅ Retrieval pipeline — cross-company querying with source citations
✅ Streamlit UI — company selector, question input, grounded answers
🚧 Deployment — coming soon
🚧 10-Q quarterly filings — coming soon

---

## About the Name

Avuna (అవున) is a Telugu word meaning *"yes"* or *"really?"* — the response you get when you finally find the answer buried in a financial filing.

---

## Author

**Kushal Paritala** — [GitHub](https://github.com/kushalparitala-kp)
