import asyncio
import logging
from app.rag import answer_query

queries = [
    "packaged drinking water",
    "cement",
    "toys",
    "laptop",
    "protective helmet",
    "IS 14543",
    "IS 13252",
    "certification",
    "testing"
]

print("--- SMOKE TESTS ---")
for q in queries:
    res = answer_query(q, "en")
    ans_snippet = res['answer'][:80].replace('\n', ' ')
    sources = [s['standard_number'] for s in res.get('sources', []) if 'standard_number' in s]
    print(f"[{q}] -> Confidence: {res['confidence']}, Sources: {sources}")
    print(f"    Answer: {ans_snippet}...")
