import os
import json
import pytest
from app.rag import find_standard_for_product
from app import knowledge_base

@pytest.fixture(scope="module")
def benchmark_data():
    benchmark_path = os.path.join(os.path.dirname(__file__), "..", "evaluation", "phase2e_benchmark.json")
    with open(benchmark_path, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture(scope="module")
def kb_records():
    return {r["id"]: r for r in knowledge_base.all_records()}

@pytest.fixture(autouse=True)
def enable_hybrid(monkeypatch):
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(dotenv_path=env_path)
    monkeypatch.setenv("USE_HYBRID_RETRIEVAL", "true")
    monkeypatch.setenv("EMBEDDING_DIMENSION", "768")
    import app.rag
    monkeypatch.setattr(app.rag, "USE_HYBRID_RETRIEVAL", True)

    import app.embeddings
    monkeypatch.setattr(app.embeddings, "EMBEDDING_DIMENSION", 768)
    if "GEMINI_API_KEY" in os.environ:
        from google import genai
        monkeypatch.setattr(app.embeddings, "_CLIENT", genai.Client(api_key=os.environ["GEMINI_API_KEY"]))

def test_benchmark_loads_correctly(benchmark_data):
    assert len(benchmark_data) >= 120
    assert any(c["category"] == "valid" for c in benchmark_data)
    assert any(c["category"] == "paraphrase" for c in benchmark_data)
    assert any(c["category"] == "exact_id" for c in benchmark_data)
    assert any(c["category"] == "generic" for c in benchmark_data)
    assert any(c["category"] == "adversarial" for c in benchmark_data)
    assert any(c["category"] == "hindi" for c in benchmark_data)
    assert any(c["category"] == "marathi" for c in benchmark_data)

def test_benchmark_expected_record_ids_exist(benchmark_data, kb_records):
    for case in benchmark_data:
        if case["expected_record_id"] is not None:
            assert case["expected_record_id"] in kb_records, f"Record ID {case['expected_record_id']} not found in KB"

def test_generic_queries_reject(benchmark_data):
    generic_cases = [c for c in benchmark_data if c["category"] == "generic"]
    for case in generic_cases:
        result = find_standard_for_product(case["query"], language=case["language"])
        assert result is None, f"Generic query '{case['query']}' incorrectly returned a match"

def test_adversarial_queries_reject(benchmark_data):
    adversarial_cases = [c for c in benchmark_data if c["category"] == "adversarial"]
    for case in adversarial_cases:
        result = find_standard_for_product(case["query"], language=case["language"])
        assert result is None, f"Adversarial query '{case['query']}' incorrectly returned a match"

def test_exact_is_number_queries_resolve(benchmark_data):
    exact_id_cases = [c for c in benchmark_data if c["category"] == "exact_id"]
    for case in exact_id_cases:
        result = find_standard_for_product(case["query"], language=case["language"])
        assert result is not None, f"Exact ID query '{case['query']}' returned No Match"
        assert case["expected_standard_number"] in result.get("standard_number", ""), \
            f"Query '{case['query']}' returned wrong standard: {result.get('standard_number')}"
