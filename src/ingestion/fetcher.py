"""
fetcher.py — fetches SEC filings for a given ticker using edgartools.

Usage:
    from src.ingestion.fetcher import fetch_filing
    date, text = fetch_filing("AAPL", form="10-K")
"""

import sys
import os

# Allow imports from the project root (e.g., "import config")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import config  # sets EDGAR identity as a side effect

from edgar import Company

# The 10 companies we support — maps ticker to readable name
COMPANIES = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "AMZN": "Amazon",
    "GOOGL": "Alphabet",
    "META": "Meta",
    "TSLA": "Tesla",
    "AVGO": "Broadcom",
    "JPM": "JPMorgan",
    "UNH": "UnitedHealth",
}


def fetch_filing(ticker: str, form: str = "10-K") -> dict:
    """
    Fetch the latest filing of a given form type for a ticker.

    Returns a dict with:
        ticker      — e.g. "AAPL"
        company     — e.g. "Apple"
        form        — e.g. "10-K"
        date        — filing date as a string, e.g. "2024-11-01"
        text        — full plain text of the filing
    """
    if ticker not in COMPANIES:
        raise ValueError(f"{ticker} is not in the supported company list: {list(COMPANIES.keys())}")

    company = Company(ticker)
    filings = company.get_filings(form=form)
    filing = filings.latest(1)

    text = filing.text()
    date = str(filing.filing_date)

    return {
        "ticker": ticker,
        "company": COMPANIES[ticker],
        "form": form,
        "date": date,
        "text": text,
    }
