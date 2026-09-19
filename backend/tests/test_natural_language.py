import os
os.environ["USE_HYBRID_RETRIEVAL"] = "true"

import pytest
from unittest.mock import patch
from app.decision import generate_compliance_response
from app.rag import answer_query
from app.models import ComplianceResponse

def test_1_natural_language_bis_query():
    # A natural language query about a specific general topic (Licensing)
    res = generate_compliance_response("How can I apply for a BIS license?", language="en")
    assert res.match_found is False
    assert res.applicable_standard in ["", "N/A"]

@patch("app.llm.is_llm_configured", return_value=True)
@patch("app.llm.extract_query_context")
def test_2_hindi_response(mock_extract, mock_is_configured):
    # Mock the LLM translating the query to English
    mock_extract.return_value = {
        "normalized_query": "What is the standard for packaged drinking water?",
        "product_entity": "packaged drinking water",
        "service_entity": "standard",
        "confidence": 1.0,
        "reason": "Clear product"
    }
    res = answer_query("पैकेज्ड पीने के पानी के लिए मानक क्या है?", language="hi")
    ans = res["answer"]
    assert "14543" in ans or "14543" in res["standard_number"]
    assert res["matched_topic"] == "Food & Beverage / Packaged Water"

@patch("app.llm.is_llm_configured", return_value=True)
@patch("app.llm.extract_query_context")
def test_3_marathi_response(mock_extract, mock_is_configured):
    mock_extract.return_value = {
        "normalized_query": "What is the standard for pressure cooker?",
        "product_entity": "pressure cooker",
        "service_entity": "standard",
        "confidence": 1.0,
        "reason": "Clear product"
    }
    # "What is the standard for pressure cooker?" in Marathi
    res = answer_query("प्रेशर कुकरसाठी मानक काय आहे?", language="mr")
    assert "2347" in res["answer"] or "2347" in res["standard_number"]
    assert res["matched_topic"] == "Household Appliances"

def test_4_english_response():
    res = answer_query("What standard applies to domestic pressure cookers?", language="en")
    assert "IS 2347" in res["answer"] or "IS 2347" in res["standard_number"]
    assert res["matched_topic"] == "Household Appliances"

@patch("app.llm.is_llm_configured", return_value=True)
@patch("app.llm.extract_query_context")
def test_5_unsupported_query_no_verified_match(mock_extract, mock_is_configured):
    mock_extract.return_value = {
        "normalized_query": "What is the certification for flying cars?",
        "product_entity": "flying cars",
        "service_entity": "certification",
        "confidence": 1.0,
        "reason": "Unknown product"
    }
    # Unsupported query that should fall back
    res = generate_compliance_response("What is the certification for flying cars?", language="en")
    assert res.match_found is False
    assert "No verified match" in res.compliance_status[0]

    # Unsupported query in Assistant flow
    res2 = answer_query("Tell me about alien UFO certification standards", language="en")
    assert "I couldn't find a verified match" in res2["answer"]

def test_6_no_hallucinated_fees_or_urls():
    # The LLM shouldn't hallucinate URLs. But since we test without API key or with mock,
    # we just ensure the deterministic source urls are exactly what is in KB.
    res = answer_query("What is hallmarking?", language="en")
    for source in res["sources"]:
        assert source["source_url"].startswith("http") or source["source_url"] == ""
        # We ensure it doesn't invent fake gov sites in the deterministic record
        assert "bis.gov.in" in source["source_url"] or "manakonline.in" in source["source_url"] or "crsbis.in" in source["source_url"]
