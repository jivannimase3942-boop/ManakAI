import pytest
from unittest.mock import patch
from app.rag import find_standard_for_product
from app import rag

@pytest.fixture(autouse=True)
def setup_hybrid():
    old_val = rag.USE_HYBRID_RETRIEVAL
    rag.USE_HYBRID_RETRIEVAL = True

    # Mock semantic retrieval to return high scores for expected records
    # This prevents the test from requiring a live Gemini API key or valid embedding cache
    def mock_sem(query, top_k=5):
        q = query.lower()
        if "सीमेंट" in q or "सिमेंट" in q or "cement" in q:
            return [{"record_id": "kb-011", "similarity": 0.85}]
        if "खिलौनों" in q or "खेळण्यां" in q or "toy" in q:
            return [{"record_id": "kb-010", "similarity": 0.85}]
        if "वाटर" in q or "वॉटर" in q or "water" in q or "पानी" in q or "पाण्या" in q:
            return [{"record_id": "kb-001", "similarity": 0.85}]
        if "हेलमेट" in q or "हेल्मेट" in q or "helmet" in q:
            return [{"record_id": "kb-013", "similarity": 0.85}]
        if "कुकर" in q or "cooker" in q:
            return [{"record_id": "kb-014", "similarity": 0.85}]
        return []

    with patch('app.hybrid_retriever.get_semantic_candidates', side_effect=mock_sem):
        yield

    rag.USE_HYBRID_RETRIEVAL = old_val

def test_successful_normalization():
    # Representative cases
    cases = [
        ("पैकेज्ड पीने के पानी के लिए बीआईएस मानक क्या है?", "hi", "kb-001", "packaged drinking water"),
        ("पॅकेज्ड पिण्याच्या पाण्यासाठी बीआयएस मानक काय आहे?", "mr", "kb-001", "packaged drinking water"),
        ("सीमेंट के लिए कौन सा BIS मानक लागू है?", "hi", "kb-011", "cement"),
        ("सिमेंटसाठी कोणता BIS मानक लागू आहे?", "mr", "kb-011", "cement"),
        ("क्या बच्चों के खिलौने सुरक्षित हैं?", "hi", "kb-010", "toys"),
        ("मुलांची खेळणी सुरक्षित आहेत का?", "mr", "kb-010", "toys"),
        ("हेलमेट का IS नंबर क्या है?", "hi", "kb-013", "protective helmet"),
        ("दुचाकी हेल्मेट प्रमाणपत्र", "mr", "kb-013", "protective helmet"),
        ("प्रेशर कुकर की सुरक्षा मानक क्या है?", "hi", "kb-014", "pressure cooker"),
        ("प्रेशर कुकर सुरक्षा मानक", "mr", "kb-014", "pressure cooker"),
    ]

    for query, lang, expected_id, product_entity in cases:
        # We mock the LLM to return exactly this normalized entity
        mock_resp = {
            "normalized_query": f"{product_entity} certification",
            "product_entity": product_entity,
            "service_entity": "certification",
            "confidence": 0.95,
            "reason": "Clear product entity identified"
        }

        # Mock semantic candidates so GATE 6 (degraded mode) doesn't block it when API key is missing
        mock_sem = [{"record_id": expected_id, "similarity": 0.8}]

        with patch('app.llm.extract_query_context', return_value=mock_resp):
            with patch('app.hybrid_retriever.get_semantic_candidates', return_value=mock_sem):
                # We also mock LLM config to True to trigger the path
                with patch('app.llm.is_llm_configured', return_value=True):
                    result = find_standard_for_product(query, language=lang)
                    assert result is not None, f"Query '{query}' returned None"
                    assert result["sources"][0]["id"] == expected_id, f"Query '{query}' mismatched"


def test_llm_failures():
    # Failure cases should safely return None (No Verified Match)
    query = "क्या यह सुरक्षित है?" # A query that natively fails the entity gate due to language

    failure_mocks = [
        {}, # Empty response / malformed / exception
        {"normalized_query": "toys", "product_entity": "toys", "service_entity": "", "confidence": 0.3}, # Low confidence
        {"normalized_query": "aircraft", "product_entity": "aircraft", "service_entity": "", "confidence": 0.9}, # Unrelated/Unknown
    ]

    for mock_resp in failure_mocks:
        with patch('app.llm.extract_query_context', return_value=mock_resp):
            with patch('app.llm.is_llm_configured', return_value=True):
                result = find_standard_for_product(query, language="hi")
                # Because the native fallback will still fail the Entity Compatibility gate (< 0.72),
                # and the LLM normalization is invalid/low-confidence/generic, it should return None.
                assert result is None, f"Expected None for mock {mock_resp}, got {result}"

def test_llm_exception_handling():
    query = "क्या यह सुरक्षित है?"

    # 429 or Timeout -> extract_query_context raises or returns {}
    def mock_raise(*args, **kwargs):
        raise Exception("429 Quota Exceeded")

    # We patch at the top level of generate_content if we were calling it,
    # but since rag calls extract_query_context, we can mock it directly to simulate exception bubbling
    # Wait, extract_query_context catches exceptions and returns {}.
    # So we simulate extract_query_context returning {}.
    with patch('app.llm.extract_query_context', return_value={}):
        with patch('app.llm.is_llm_configured', return_value=True):
            result = find_standard_for_product(query, language="hi")
            assert result is None
