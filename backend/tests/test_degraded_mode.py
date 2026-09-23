import pytest
from app.hybrid_retriever import hybrid_search
import os

# Set fake API key to simulate degraded mode
os.environ["GEMINI_API_KEY"] = "FAKE"

def test_degraded_mode_marathi_cooker():
    records = hybrid_search('?????? ISI ?????', top_k=3, norm_context={'normalized_query': 'cooker isi mark', 'product_entity': 'cooker'})
    assert len(records) == 0

def test_degraded_mode_marathi_water():
    records = hybrid_search('?????????? ????????? ?????? ????? ??? ????????', top_k=3, norm_context={'normalized_query': 'how to check isi mark on water bottle', 'product_entity': 'water bottle'})
    assert len(records) == 0

def test_degraded_mode_exact_id_works():
    # Exact ID queries should still work even in degraded mode because is_exact_id = True skips GATE 6
    records = hybrid_search('IS 14543', top_k=3, norm_context={'normalized_query': 'is 14543', 'product_entity': 'water'})
    assert len(records) > 0
    assert records[0]['id'] == 'kb-001'
