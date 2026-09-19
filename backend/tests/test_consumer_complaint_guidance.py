import pytest
from app.rag import answer_query

def test_ccg_known_complaint_returns_verified_data():
    """
    Test that a known consumer complaint query returns correct procedural guidance.
    """
    result = answer_query("how to file a consumer complaint", "en")

    assert result is not None
    assert result.get("confidence") != "none"

    content = result.get("answer", "").lower()
    assert "bis care app" in content or "portal" in content or "complaint" in content
    assert len(result.get("sources", [])) > 0

def test_ccg_unknown_complaint_returns_no_verified_match():
    """
    Test that an unrelated or unverified complaint safely falls back to NO VERIFIED MATCH.
    """
    result = answer_query("how to report bad airplane food to the airline", "en")

    assert result is not None
    if result.get("confidence") != "none":
        assert "no verified match" in result.get("answer", "").lower()
    else:
        assert result.get("confidence") == "none"

def test_ccg_does_not_fabricate_urls_or_outcomes():
    """
    Ensure the structured response does not invent unauthorized URLs or guarantee case outcomes.
    """
    result = answer_query("what happens if i complain about packaged drinking water", "en")

    assert result is not None

    content = result.get("answer", "").lower()
    assert "fakeurl.com" not in content, "Should not fabricate URLs"
    assert "guarantee" not in content and "100% refund" not in content, "Should not hallucinate outcomes"
