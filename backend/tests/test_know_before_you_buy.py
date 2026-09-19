import pytest
from app.rag import find_standard_for_product

def test_kbyb_known_product_returns_verified_data():
    """
    Test that a known product returns the correct standard and mark
    for a consumer 'Know Before You Buy' scenario.
    """
    result = find_standard_for_product("pressure cooker", "en")

    assert result is not None
    assert result.get("confidence") != "none"
    assert (result.get("applicable_standard") and "IS 2347" in result.get("applicable_standard")) or (result.get("standard_number") and "IS 2347" in result.get("standard_number"))
    assert "ISI Mark" in str(result) or len(result.get("sources", [])) > 0

def test_kbyb_unknown_product_returns_no_verified_match():
    """
    Test that an unknown/unverified product safely falls back to NO VERIFIED MATCH
    (confidence='none' or None) instead of hallucinating consumer guidance.
    """
    result = find_standard_for_product("hoverboard certification", "en")

    if result is not None:
        assert result.get("confidence") == "none"
    else:
        assert result is None

def test_kbyb_does_not_fabricate_urls_or_fees():
    """
    Ensure the structured response does not invent unauthorized fees or URLs
    when giving consumer guidance.
    """
    result = find_standard_for_product("packaged drinking water", "en")

    assert result is not None
    assert result.get("applicable_standard") in ["IS 14543", "IS 14543:2024"] or result.get("standard_number") in ["IS 14543", "IS 14543:2024"]

    # Verify no fake fee information is injected into standard RAG responses
    content = str(result).lower()
    assert "rupees" not in content and "₹" not in content, "Should not fabricate fees"
    assert "fakeurl.com" not in content, "Should not fabricate URLs"
