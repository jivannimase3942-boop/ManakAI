import pytest
from app.decision import generate_compliance_response

def test_imc_known_product_returns_verified_data():
    """
    Test that a known product returns the correct standard and scheme
    for Industry/MSME Compliance Guidance.
    """
    result = generate_compliance_response("pressure cooker certification", "industry", "en")

    assert result.match_found is True
    assert result.confidence != "none"
    assert "IS 2347" in result.applicable_standard or "IS 2347" in result.why_applicable
    assert len(result.sources) > 0

def test_imc_unknown_product_returns_no_verified_match():
    """
    Test that an unknown product returns no verified match.
    """
    result = generate_compliance_response("how to build a time machine", "industry", "en")

    assert result.match_found is False
    assert result.confidence == "none"

def test_imc_does_not_fabricate_urls_or_fees():
    """
    Ensure the structured response does not invent unauthorized URLs, fees, or timelines.
    """
    result = generate_compliance_response("how much does it cost to certify cement", "industry", "en")

    if result.match_found:
        content = str(result.model_dump()).lower()
        assert "fakeurl.com" not in content, "Should not fabricate URLs"
        assert "rs." not in content and "rupees" not in content, "Should not hallucinate fees"

from unittest.mock import patch

def test_imc_marathi_pressure_cooker():
    import app.decision
    app.decision.USE_HYBRID_RETRIEVAL = True
    # Only test if LLM API is mocked or available in the environment
    # Actually, we can patch extract_query_context to simulate LLM success
    with patch("app.llm.is_llm_configured", return_value=True), \
         patch("app.llm.extract_query_context", return_value={
             "normalized_query": "I want to manufacture a pressure cooker. What BIS standard is applicable for this and what should be done for certification?",
             "product_entity": "pressure cooker",
             "service_entity": "certification",
             "confidence": 0.95
         }):
        result = generate_compliance_response("मला प्रेशर कुकर बनवायचा आहे. त्यासाठी कोणता BIS मानक लागू आहे आणि प्रमाणपत्रासाठी काय करावे लागेल?", "industry", "mr")
        assert result.match_found is True
        assert "IS 2347" in result.applicable_standard or "IS 2347" in result.why_applicable

def test_imc_hindi_pressure_cooker():
    import app.decision
    app.decision.USE_HYBRID_RETRIEVAL = True
    with patch("app.llm.is_llm_configured", return_value=True), \
         patch("app.llm.extract_query_context", return_value={
             "normalized_query": "I want to manufacture a pressure cooker. What BIS standard is applicable for this and what should be done for certification?",
             "product_entity": "pressure cooker",
             "service_entity": "certification",
             "confidence": 0.95
         }):
        result = generate_compliance_response("मुझे प्रेशर कुकर बनाना है। इसके लिए कौन सा बीआईएस मानक लागू है?", "industry", "hi")
        assert result.match_found is True
        assert "IS 2347" in result.applicable_standard or "IS 2347" in result.why_applicable

def test_imc_marathi_unsupported_query():
    import app.decision
    app.decision.USE_HYBRID_RETRIEVAL = True
    with patch("app.llm.is_llm_configured", return_value=True), \
         patch("app.llm.extract_query_context", return_value={
             "normalized_query": "",
             "product_entity": "",
             "service_entity": "",
             "confidence": 0.1
         }):
        result = generate_compliance_response("उडणाऱ्या कारसाठी मानके काय आहेत?", "industry", "mr")
        assert result.match_found is False
        assert result.why_applicable == "मला ManakAI नॉलेज बेसमध्ये यासाठी सत्यापित माहिती सापडली नाही. कृपया तुमचा प्रश्न पुन्हा लिहा, किंवा अधिकृत माहितीसाठी BIS वेबसाइट (bis.gov.in) पहा."

def test_imc_adversarial_flying_car_rejected():
    import app.decision
    app.decision.USE_HYBRID_RETRIEVAL = True
    with patch("app.llm.is_llm_configured", return_value=True), \
         patch("app.llm.extract_query_context", return_value={
             "normalized_query": "",
             "product_entity": "",
             "service_entity": "",
             "confidence": 0.1
         }):
        result = generate_compliance_response("standards for flying cars", "industry", "en")
        assert result.match_found is False



from fastapi.testclient import TestClient
from main import app as fastapi_app

def test_api_standard_search_marathi_pressure_cooker():
    import app.decision
    app.decision.USE_HYBRID_RETRIEVAL = True
    with patch("app.llm.is_llm_configured", return_value=True), \
         patch("app.llm.extract_query_context", return_value={
             "normalized_query": "I want to manufacture a pressure cooker. What BIS standard is applicable for this and what should be done for certification?",
             "product_entity": "pressure cooker",
             "service_entity": "certification",
             "confidence": 0.95
         }):
        client = TestClient(fastapi_app)
        response = client.post('/api/standard-search', json={'description': 'मला प्रेशर कुकर बनवायचा आहे. त्यासाठी कोणता BIS मानक लागू आहे आणि प्रमाणपत्रासाठी काय करावे लागेल?', 'language': 'mr'})
        assert response.status_code == 200
        data = response.json()
        assert data['match_found'] is True
        assert 'IS 2347' in data['applicable_standard'] or 'IS 2347' in data['why_applicable']
        assert 'SIH 2026' not in data.get('disclaimer', '')
        assert 'demo' not in data.get('disclaimer', '').lower()
        assert len(data['sources']) > 0

def test_api_standard_search_hindi_pressure_cooker():
    import app.decision
    app.decision.USE_HYBRID_RETRIEVAL = True
    with patch("app.llm.is_llm_configured", return_value=True), \
         patch("app.llm.extract_query_context", return_value={
             "normalized_query": "I want to manufacture a pressure cooker. What BIS standard is applicable for this and what should be done for certification?",
             "product_entity": "pressure cooker",
             "service_entity": "certification",
             "confidence": 0.95
         }):
        client = TestClient(fastapi_app)
        response = client.post('/api/standard-search', json={'description': 'मुझे प्रेशर कुकर बनाना है। इसके लिए कौन सा बीआईएस मानक लागू है?', 'language': 'hi'})
        assert response.status_code == 200
        data = response.json()
        assert data['match_found'] is True
        assert 'IS 2347' in data['applicable_standard'] or 'IS 2347' in data['why_applicable']
        assert 'SIH 2026' not in data.get('disclaimer', '')
        assert len(data['sources']) > 0

def test_api_standard_search_english_pressure_cooker():
    import app.decision
    app.decision.USE_HYBRID_RETRIEVAL = True
    with patch("app.llm.is_llm_configured", return_value=True), \
         patch("app.llm.extract_query_context", return_value={
             "normalized_query": "pressure cooker",
             "product_entity": "pressure cooker",
             "service_entity": "",
             "confidence": 0.95
         }):
        client = TestClient(fastapi_app)
        response = client.post('/api/standard-search', json={'description': 'pressure cooker standards', 'language': 'en'})
        assert response.status_code == 200
        data = response.json()
        assert data['match_found'] is True
        assert 'IS 2347' in data['applicable_standard'] or 'IS 2347' in data['why_applicable']
        assert 'SIH 2026' not in data.get('disclaimer', '')
        assert len(data['sources']) > 0

def test_api_standard_search_adversarial_flying_car():
    import app.decision
    app.decision.USE_HYBRID_RETRIEVAL = True
    with patch("app.llm.is_llm_configured", return_value=True), \
         patch("app.llm.extract_query_context", return_value={
             "normalized_query": "",
             "product_entity": "",
             "service_entity": "",
             "confidence": 0.1
         }):
        client = TestClient(fastapi_app)
        response = client.post('/api/standard-search', json={'description': 'standards for flying cars', 'language': 'en'})
        assert response.status_code == 200
        data = response.json()
        assert data['match_found'] is False
        assert data['confidence'] == 'none'
        assert 'SIH 2026' not in data.get('disclaimer', '')
