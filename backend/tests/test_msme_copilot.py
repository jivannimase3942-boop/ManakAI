from app.rag import find_standard_for_product
from app.hybrid_retriever import hybrid_search

def test_msme_copilot_explicit_context_allows_match():
    # When MSME manufacturer explicitly provides a product, it should route correctly
    res = find_standard_for_product("I manufacture electric ceiling fans, what do I need?", language="en")
    assert res is not None
    assert "IS 374" in res["standard_number"]

def test_msme_copilot_generic_context_is_rejected():
    # Even if MSME manufacturer mentions services, without product it should be rejected by global safety
    res = find_standard_for_product("I am an MSME manufacturer, how do I apply for a testing laboratory?", language="en")
    assert res is None
