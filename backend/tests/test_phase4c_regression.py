import pytest
from app.rag import find_standard_for_product

def test_generic_queries_reject():
    generics = [
        "where is the laboratory",
        "where are BIS laboratories",
        "tell me about laboratories",
        "where can testing be done"
    ]
    for q in generics:
        res = find_standard_for_product(q, language="en")
        assert res is None, f"Generic query '{q}' should be rejected."

def test_specific_product_service_queries():
    specifics = [
        ("pressure cooker testing", "kb-014"),
        ("where can pressure cooker be tested", "kb-014"),
        ("laboratory for pressure cooker", "kb-014"),
        ("mobile phone BIS certification", "kb-019")
    ]
    for q, expected in specifics:
        res = find_standard_for_product(q, language="en")
        assert res is not None, f"Specific query '{q}' returned None."
        assert res["sources"][0]["id"] == expected, f"Specific query '{q}' returned {res['sources'][0]['id']} instead of {expected}."
