import pytest
from unittest.mock import patch
from app.rag import answer_query, _llm_answer

# We mock LLM generate directly to test the system prompt behavior and the interception logic.

@patch('app.rag.hybrid_retriever.hybrid_search')
@patch('app.rag.llm.generate')
@patch('app.rag.llm.is_llm_configured', return_value=True)
def test_strict_grounding_unsupported_query(mock_is_configured, mock_generate, mock_search):
    # If the LLM determines context is insufficient and returns NO VERIFIED MATCH
    mock_generate.return_value = "NO VERIFIED MATCH"

    # Mock search to return a generic record to ensure we reach the LLM logic
    mock_search.return_value = [{"title": "Test", "summary": "Test summary", "topic": "test", "source_name": "Test", "source_url": "test.com"}]

    # "What is the certification for alien spaceships?"
    res = answer_query("What is the certification for alien spaceships?", language="en")

    # answer_query should intercept "NO VERIFIED MATCH" and return the NO_MATCH_TEXT
    assert res["matched_topic"] is None
    assert "I couldn't find a verified match" in res["answer"]
    assert res["mode"] == "llm"

@patch('app.rag.llm.generate')
@patch('app.rag.llm.is_llm_configured', return_value=True)
def test_strict_evidence_and_language_english(mock_is_configured, mock_generate):
    mock_generate.return_value = "According to BIS official documentation, hallmarking is mandatory. (Source: BIS website)"

    res = answer_query("What is hallmarking?", language="en")
    assert "According to BIS official documentation" in res["answer"]
    assert res["mode"] == "llm"

@patch('app.rag.llm.generate')
@patch('app.rag.llm.is_llm_configured', return_value=True)
def test_strict_evidence_and_language_hindi(mock_is_configured, mock_generate):
    # Testing translation and interception in Hindi
    mock_generate.return_value = "NO VERIFIED MATCH"

    res = answer_query("एलियन स्पेसशिप के लिए मानक क्या है?", language="hi")
    assert res["matched_topic"] is None
    # Verify the Hindi NO_MATCH_TEXT is returned
    assert "मुझे ManakAI" in res["answer"] or "जानकारी नहीं मिली" in res["answer"]

@patch('app.rag.llm.generate')
@patch('app.rag.llm.is_llm_configured', return_value=True)
def test_strict_evidence_and_language_marathi(mock_is_configured, mock_generate):
    # Testing translation and interception in Marathi
    mock_generate.return_value = "NO VERIFIED MATCH"

    res = answer_query("एलियन स्पेसशिपसाठी मानक काय आहे?", language="mr")
    assert res["matched_topic"] is None
    # Verify the Marathi NO_MATCH_TEXT is returned
    assert "मला ManakAI" in res["answer"] or "माहिती आढळली नाही" in res["answer"]

def test_system_prompt_hardened():
    records = [{"title": "Test", "summary": "Test summary", "source_name": "Test Source", "source_url": "test.com"}]
    with patch('app.rag.llm.generate') as mock_generate:
        _llm_answer("What is this?", records, "en")
        system_prompt_used = mock_generate.call_args[0][0]
        assert "exactly 'NO VERIFIED MATCH'" in system_prompt_used
        assert "Never invent" in system_prompt_used
        assert "explicitly expose its verified source" in system_prompt_used
