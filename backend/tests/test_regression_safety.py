import os
import pytest
from app.rag import find_standard_for_product

@pytest.fixture(autouse=True)
def enable_hybrid(monkeypatch):
    from dotenv import load_dotenv
    import os
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(dotenv_path=env_path)
    monkeypatch.setenv("USE_HYBRID_RETRIEVAL", "true")
    import app.rag
    monkeypatch.setattr(app.rag, "USE_HYBRID_RETRIEVAL", True)

    import app.embeddings
    if "GEMINI_API_KEY" in os.environ:
        from google import genai
        monkeypatch.setattr(app.embeddings, "_CLIENT", genai.Client(api_key=os.environ["GEMINI_API_KEY"]))

    import app.hybrid_retriever
    def mock_sem(query, *args, **kwargs):
        q = query.lower()
        if "cement" in q: return [{"record_id": "kb-011", "similarity": 0.85}]
        if "toys" in q: return [{"record_id": "kb-010", "similarity": 0.85}]
        if "laptop" in q: return [{"record_id": "kb-012", "similarity": 0.85}]
        if "water" in q: return [{"record_id": "kb-001", "similarity": 0.85}]
        if "steel" in q or "rebar" in q: return [{"record_id": "kb-015", "similarity": 0.85}]
        if "lpg" in q or "cylinder" in q: return [{"record_id": "kb-016", "similarity": 0.85}]
        return []
    monkeypatch.setattr(app.hybrid_retriever, "get_semantic_candidates", mock_sem)

def test_regression_certification_no_match():
    assert not find_standard_for_product("certification")

def test_regression_testing_no_match():
    assert not find_standard_for_product("testing")

def test_regression_aircraft_certification_no_match():
    assert not find_standard_for_product("aircraft certification")

def test_regression_flying_car_certification_no_match():
    assert not find_standard_for_product("flying car certification")

def test_regression_random_unknown_product_no_match():
    assert not find_standard_for_product("random unknown product")

def test_regression_cement_match():
    record = find_standard_for_product("cement")
    assert record
    assert "cement" in record.get("title", "").lower()

def test_regression_toys_match():
    record = find_standard_for_product("toys")
    assert record
    assert "toys" in record.get("title", "").lower()

def test_regression_laptop_match():
    record = find_standard_for_product("laptop")
    assert record
    assert "information technology" in record.get("title", "").lower() or "laptop" in record.get("title", "").lower()

def test_regression_packaged_drinking_water_match():
    record = find_standard_for_product("packaged drinking water")
    assert record
    assert "14543" in record.get("standard_number", "")

def test_regression_exact_standard_match():
    record = find_standard_for_product("IS 14543")
    assert record
    assert "14543" in record.get("standard_number", "")

def test_regression_steel_rebars_match():
    record = find_standard_for_product("steel rebars")
    assert record
    assert "1786" in record.get("standard_number", "")

def test_regression_lpg_cylinders_match():
    record = find_standard_for_product("lpg cylinders")
    assert record
    assert "3196" in record.get("standard_number", "")

def test_decision_engine_required_documents_omitted(monkeypatch):
    import app.decision
    # Test that when required_documents is empty in DB, it safely remains empty in response
    resp = app.decision.generate_compliance_response("toys", mode="consumer", language="en")
    assert resp.match_found is True
    assert resp.required_documents == []

def test_decision_engine_required_documents_surfaced(monkeypatch):
    import app.decision
    import app.hybrid_retriever

    original_search = app.hybrid_retriever.hybrid_search

    def mock_hybrid_search(query, top_k=1):
        # Inject fake required documents just for testing the propagation
        records = original_search(query, top_k)
        if records:
            records[0]["required_documents"] = ["Test Form 1", "Test Registration"]
        return records

    monkeypatch.setattr(app.hybrid_retriever, "hybrid_search", mock_hybrid_search)
    resp = app.decision.generate_compliance_response("toys", mode="consumer", language="en")
    assert resp.match_found is True
    assert resp.required_documents == ["Test Form 1", "Test Registration"]
