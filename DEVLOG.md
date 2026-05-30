# Avuna — Dev Log

A running journal of decisions, progress, and problems solved.

---

## May 29, 2026

**Full working RAG system built end to end.**

- Set up project scaffold, virtual environment, all dependencies
- Connected EDGAR, Pinecone, and Groq — all 3 verified
- Built ingestion pipeline: fetch → chunk → embed → Pinecone upsert
- Ingested all 10 S&P 500 companies — 1,684 vectors in Pinecone
- Built retrieval pipeline: question → Pinecone search → Groq answer
- Built Streamlit UI with company checkboxes and cross-company querying
- Apple revenue query returned exact figure: $416,161 million
- Tech stack: Python, edgartools, LlamaIndex, Pinecone, Groq, Streamlit

**Next session:** Read through all code files, deploy to public URL, add 10-Q filings

---

## May 26, 2026

**Project kickoff.**

- Named project Avuna (Telugu for "yes/really?" — the response when you find the answer)
- Defined project scope: RAG system on SEC EDGAR filings for top 10 S&P 500 companies
- Wrote README
- Tech stack finalized: Python, edgartools, LlamaIndex, Pinecone, Groq, Streamlit
- Created GitHub repo at github.com/kushalparitala-kp/Avuna
