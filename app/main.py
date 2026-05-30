"""
main.py — Streamlit UI for Avuna.

Run:
    source venv/bin/activate
    streamlit run app/main.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from src.retrieval.query import query
from src.ingestion.fetcher import COMPANIES

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Avuna — SEC Filing Intelligence",
    page_icon="📋",
    layout="wide",
)

# ── Session state: initialise all checkboxes to True on first load ─────────────
if "checkboxes_init" not in st.session_state:
    for ticker in COMPANIES:
        st.session_state[f"cb_{ticker}"] = True
    st.session_state.checkboxes_init = True

# ── Sidebar: company selector ─────────────────────────────────────────────────
with st.sidebar:
    st.title("📋 Avuna")
    st.caption("SEC Filing Intelligence")
    st.divider()

    st.subheader("Companies")
    st.caption("Select which filings to search")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Select All", use_container_width=True):
            for ticker in COMPANIES:
                st.session_state[f"cb_{ticker}"] = True
            st.rerun()
    with col2:
        if st.button("Clear All", use_container_width=True):
            for ticker in COMPANIES:
                st.session_state[f"cb_{ticker}"] = False
            st.rerun()

    st.markdown("")
    for ticker, name in COMPANIES.items():
        st.checkbox(f"{name} ({ticker})", key=f"cb_{ticker}")

    st.divider()
    st.caption("Data: SEC EDGAR 10-K filings\nLLM: Groq llama-3.3-70b\nEmbeddings: all-MiniLM-L6-v2")

# ── Main area ─────────────────────────────────────────────────────────────────
st.header("Ask a question about SEC filings")
st.caption("Searches the latest 10-K filings for the selected companies.")

question = st.text_area(
    label="Your question",
    placeholder="e.g. What was Apple's total revenue in 2025?\ne.g. Compare the main risks faced by Microsoft and NVIDIA.\ne.g. Which company has the highest R&D spending?",
    height=100,
    label_visibility="collapsed",
)

ask_clicked = st.button("Ask", type="primary", use_container_width=False)

if ask_clicked:
    # Collect selected tickers
    selected_tickers = [t for t in COMPANIES if st.session_state.get(f"cb_{t}", False)]

    if not question.strip():
        st.warning("Please enter a question.")
    elif not selected_tickers:
        st.error("Please select at least one company in the sidebar.")
    else:
        # Pass None when all companies are selected (searches whole index, slightly faster)
        tickers_arg = None if len(selected_tickers) == len(COMPANIES) else selected_tickers

        company_labels = ", ".join(
            f"{COMPANIES[t]} ({t})" for t in selected_tickers
        )
        st.caption(f"Searching: {company_labels}")

        with st.spinner("Searching filings and generating answer..."):
            try:
                result = query(question.strip(), tickers=tickers_arg)
            except Exception as e:
                st.error(f"Query failed: {e}")
                st.stop()

        # ── Answer ────────────────────────────────────────────────────────────
        st.divider()
        st.subheader("Answer")
        st.write(result["answer"])

        # ── Sources ───────────────────────────────────────────────────────────
        st.divider()
        with st.expander(f"View sources ({len(result['sources'])} chunks retrieved)"):
            for i, s in enumerate(result["sources"], 1):
                score_pct = f"{s['score'] * 100:.1f}%" if s["score"] else "n/a"
                st.markdown(
                    f"**{i}. {s['company']} ({s['ticker']}) — {s['form']} filed {s['date']}** "
                    f"— relevance: {score_pct}"
                )
                st.caption(s["text"] + "...")
                if i < len(result["sources"]):
                    st.divider()
