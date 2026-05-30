"""
test_config.py — run this to verify all external connections work.

Usage:
    source venv/bin/activate
    python test_config.py

Each check is independent — a failure in one does not stop the others.
"""

import sys

PASS = "  [PASS]"
FAIL = "  [FAIL]"


def check_env_file():
    print("\n[1/4] Checking .env file...")
    import os
    from dotenv import load_dotenv
    load_dotenv()

    missing = []
    for key in ["PINECONE_API_KEY", "GROQ_API_KEY", "EDGAR_IDENTITY"]:
        if not os.environ.get(key):
            missing.append(key)

    if missing:
        print(f"{FAIL} Missing keys in .env: {', '.join(missing)}")
        print("       Copy .env.example to .env and fill in the values.")
        return False

    print(f"{PASS} All 3 environment variables found in .env")
    return True


def check_edgar():
    print("\n[2/4] Checking EDGAR (edgartools)...")
    try:
        import config  # this calls set_identity() as a side effect
        from edgar import Company
        company = Company("AAPL")
        print(f"{PASS} EDGAR identity set, fetched company: {company.name}")
        return True
    except Exception as e:
        print(f"{FAIL} EDGAR error: {e}")
        return False


def check_pinecone():
    print("\n[3/4] Checking Pinecone...")
    try:
        from config import pc
        indexes = pc.list_indexes()
        names = [i.name for i in indexes]
        if names:
            print(f"{PASS} Pinecone connected. Existing indexes: {names}")
        else:
            print(f"{PASS} Pinecone connected. No indexes yet (that's fine — we'll create one during ingestion).")
        return True
    except Exception as e:
        print(f"{FAIL} Pinecone error: {e}")
        return False


def check_groq():
    print("\n[4/4] Checking Groq LLM...")
    try:
        from config import llm
        response = llm.complete("Reply with exactly one word: hello")
        print(f"{PASS} Groq responded: '{response.text.strip()}'")
        return True
    except Exception as e:
        print(f"{FAIL} Groq error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Avuna — connection checks")
    print("=" * 50)

    # .env must pass before we try anything else
    if not check_env_file():
        print("\nFix .env first, then re-run this script.\n")
        sys.exit(1)

    results = [
        check_edgar(),
        check_pinecone(),
        check_groq(),
    ]

    passed = sum(results)
    total = len(results)

    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} checks passed")
    if passed == total:
        print("All connections verified. Ready to build ingestion.")
    else:
        print("Fix the failed checks above before moving on.")
    print("=" * 50 + "\n")

    sys.exit(0 if passed == total else 1)
