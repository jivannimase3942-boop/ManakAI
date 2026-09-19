import pytest
from app.decision import generate_compliance_response

from unittest.mock import patch

def test_lg_known_testing_query_returns_verified_data():
    """
    Test that a known testing query returns the correct guidance.
    """
    with patch("app.decision.hybrid_retriever.hybrid_search") as mock_hybrid:
        mock_hybrid.return_value = [{
            "title": "BIS-Recognised Testing Laboratories",
            "topic": "Testing",
            "summary": "Lab guidance",
            "testing": {"details": ["Testing must be performed at an officially recognised BIS laboratory."]},
            "_retrieval_confidence": "high"
        }]
        result = generate_compliance_response("where can i test my product", "industry", "en")

        assert result.match_found is True
        assert result.confidence != "none"
    assert "laboratory" in result.why_applicable.lower() or len(result.testing) > 0
    assert len(result.sources) > 0

def test_lg_unknown_testing_query_returns_no_verified_match():
    """
    Test that an unknown query safely falls back to NO VERIFIED MATCH.
    """
    result = generate_compliance_response("where to buy pizza in new delhi", "industry", "en")

    assert result.match_found is False
    assert result.confidence == "none"

def test_lg_does_not_fabricate_lab_names_or_fees():
    """
    Ensure the structured response does not invent unauthorized lab names or fees.
    """
    result = generate_compliance_response("what is the fee and name of the cement lab", "industry", "en")

    if result.match_found:
        content = str(result.model_dump()).lower()
        assert "fake lab" not in content, "Should not fabricate lab names"
        assert "rs." not in content and "rupees" not in content, "Should not hallucinate fees"
