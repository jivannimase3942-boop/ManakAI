import pytest
from app.rag import find_standard_for_product

def test_pvg_known_product_returns_verified_data():
    """
    Test that a known product returns the correct standard and scheme
    for a Product Verification Guidance scenario.
    """
    result = find_standard_for_product("packaged drinking water", "en")

    assert result is not None
    assert result.get("confidence") != "none"
    assert "IS 14543" in str(result)
    assert len(result.get("sources", [])) > 0

def test_pvg_unknown_product_returns_no_verified_match():
    """
    Test that an unknown/unverified product safely falls back to NO VERIFIED MATCH
    (confidence='none' or None) instead of hallucinating verification guidance.
    """
    result = find_standard_for_product("magic carpet verification", "en")

    if result is not None:
        assert result.get("confidence") == "none"
    else:
        assert result is None

def test_pvg_does_not_fabricate_live_verification_claims():
    """
    Ensure the structured response does not claim to perform live verification
    or fabricate HUID/licence validity status.
    """
    result = find_standard_for_product("gold jewelry", "en")

    assert result is not None

    content = str(result).lower()
    # Should not claim a specific licence or HUID is valid in the generalized RAG response
    assert "is valid" not in content and "authentic" not in content, "Should not claim authenticity"
    assert "live verification" not in content, "Should not claim live verification"
