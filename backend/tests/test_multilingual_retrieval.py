import pytest
import os
from dotenv import load_dotenv
load_dotenv()
from app import rag
from app.rag import find_standard_for_product

from unittest.mock import patch

@pytest.fixture(autouse=True)
def setup_hybrid():
    old_val = rag.USE_HYBRID_RETRIEVAL
    rag.USE_HYBRID_RETRIEVAL = True

    # Mock semantic retrieval to return high scores for expected records
    # This prevents the test from requiring a live Gemini API key or valid embedding cache
    def mock_sem(query, top_k=5):
        q = query.lower()
        if any(w in q for w in ["सीमेंट", "सिमेंट", "ಸಿಮೆಂಟ್", "సిమెంట్", "சிமெண்ட", "સિમેન્ટ", "cement"]):
            return [{"record_id": "kb-011", "similarity": 0.85}]
        if any(w in q for w in ["खिलौनों", "खेळण्यां", "ಆಟಿಕೆ", "బొమ్మ", "பொம்மை", "રમકડાં", "toy"]):
            return [{"record_id": "kb-010", "similarity": 0.85}]
        if any(w in q for w in ["वाटर", "वॉटर", "ನೀರಿ", "నీరు", "நீரு", "પાણી", "water"]):
            return [{"record_id": "kb-001", "similarity": 0.85}]
        return []

    with patch('app.hybrid_retriever.get_semantic_candidates', side_effect=mock_sem):
        yield

    rag.USE_HYBRID_RETRIEVAL = old_val

def test_multilingual_supported_products():
    cases = [
        # Hindi
        ("सीमेंट के लिए कौन सा BIS मानक लागू है?", "hi", "kb-011"),
        ("खिलौनों के लिए BIS मानक क्या है?", "hi", "kb-010"),
        ("पैकेज्ड ड्रिंकिंग वाटर का मानक क्या है?", "hi", "kb-001"),
        # Marathi
        ("सिमेंटसाठी कोणता BIS मानक लागू आहे?", "mr", "kb-011"),
        ("खेळण्यांसाठी BIS मानक काय आहे?", "mr", "kb-010"),
        ("पॅकेज्ड ड्रिंकिंग वॉटरसाठी कोणता मानक आहे?", "mr", "kb-001"),
        # Kannada
        ("ಸಿಮೆಂಟ್ಗಾಗಿ BIS ಮಾನದಂಡವೇನು?", "kn", "kb-011"),
        ("ಆಟಿಕೆಗಳಿಗೆ BIS ಮಾನದಂಡವೇನು?", "kn", "kb-010"),
        ("ಕುಡಿಯುವ ನೀರಿಗಾಗಿ BIS ಮಾನದಂಡವೇನು?", "kn", "kb-001"),
        # Telugu
        ("సిమెంట్ కోసం BIS ప్రమాణం ఏమిటి?", "te", "kb-011"),
        ("బొమ్మలకు BIS ప్రమాణం ఏమిటి?", "te", "kb-010"),
        ("త్రాగు నీరు కోసం BIS ప్రమాణం ఏమిటి?", "te", "kb-001"),
        # Tamil
        ("சிமெண்டிற்கான BIS தரநிலை என்ன?", "ta", "kb-011"),
        ("பொம்மைகளுக்கான BIS தரநிலை என்ன?", "ta", "kb-010"),
        ("குடிநீருக்கான BIS தரநிலை என்ன?", "ta", "kb-001"),
        # Gujarati
        ("સિમેન્ટ માટે BIS ધોરણ શું છે?", "gu", "kb-011"),
        ("રમકડાં માટે BIS ધોરણ શું છે?", "gu", "kb-010"),
        ("પીવાના પાણી માટે BIS ધોરણ શું છે?", "gu", "kb-001")
    ]

    for query, lang, expected_id in cases:
        result = find_standard_for_product(query, language=lang)
        assert result is not None, f"Query '{query}' returned None"
        assert result["sources"][0]["id"] == expected_id, f"Query '{query}' mismatched"

def test_english_paraphrases():
    cases = [
        ("drinking water testing", "kb-001"),
        ("toy safety testing", "kb-010")
    ]

    for query, expected_id in cases:
        result = find_standard_for_product(query, language="en")
        assert result is not None, f"Query '{query}' returned None"
        assert result["sources"][0]["id"] == expected_id, f"Query '{query}' mismatched"

def test_unsupported_adversarial_queries():
    cases = [
        ("aircraft certification", "en"),
        ("flying car certification", "en"),
        ("विमानासाठी प्रमाणपत्र आवश्यक आहे का?", "mr"), # Aircraft certification in Marathi
        ("विमान प्रमाणन", "hi") # Aircraft certification in Hindi
    ]

    for query, lang in cases:
        result = find_standard_for_product(query, language=lang)
        assert result is None, f"Adversarial query '{query}' incorrectly matched {result['sources'][0]['id'] if result else None}"

def test_generic_service_queries():
    cases = [
        "certification",
        "testing",
        "requirements",
        "BIS",
        "BIS standard",
        "BIS certification",
        "where is the laboratory",
        "how to apply"
    ]

    for query in cases:
        result = find_standard_for_product(query, language="en")
        assert result is None, f"Generic query '{query}' incorrectly matched {result['sources'][0]['id'] if result else None}"

def test_product_plus_service_queries():
    cases = [
        ("How can I get BIS certification for cement?", "kb-011"),
        ("Where can I test packaged drinking water?", "kb-001")
    ]

    for query, expected_id in cases:
        result = find_standard_for_product(query, language="en")
        assert result is not None, f"Product+service query '{query}' returned None"
        assert result["sources"][0]["id"] == expected_id, f"Query '{query}' mismatched"
import pytest
import os
from dotenv import load_dotenv
load_dotenv()
from app import rag
from app.rag import find_standard_for_product

from unittest.mock import patch

@pytest.fixture(autouse=True)
def setup_hybrid():
    old_val = rag.USE_HYBRID_RETRIEVAL
    rag.USE_HYBRID_RETRIEVAL = True

    # Mock semantic retrieval to return high scores for expected records
    # This prevents the test from requiring a live Gemini API key or valid embedding cache
    def mock_sem(query, top_k=5):
        q = query.lower()
        if any(w in q for w in ["सीमेंट", "सिमेंट", "ಸಿಮೆಂಟ್", "సిమెంట్", "சிமெண்ட", "સિમેન્ટ", "cement"]):
            return [{"record_id": "kb-011", "similarity": 0.85}]
        if any(w in q for w in ["खिलौनों", "खेळण्यां", "ಆಟಿಕೆ", "బొమ్మ", "பொம்மை", "રમકડાં", "toy"]):
            return [{"record_id": "kb-010", "similarity": 0.85}]
        if any(w in q for w in ["वाटर", "वॉटर", "ನೀರಿ", "నీరు", "நீரு", "પાણી", "water"]):
            return [{"record_id": "kb-001", "similarity": 0.85}]
        return []

    with patch('app.hybrid_retriever.get_semantic_candidates', side_effect=mock_sem):
        yield

    rag.USE_HYBRID_RETRIEVAL = old_val

def test_multilingual_supported_products():
    cases = [
        # Hindi
        ("सीमेंट के लिए कौन सा BIS मानक लागू है?", "hi", "kb-011"),
        ("खिलौनों के लिए BIS मानक क्या है?", "hi", "kb-010"),
        ("पैकेज्ड ड्रिंकिंग वाटर का मानक क्या है?", "hi", "kb-001"),
        # Marathi
        ("सिमेंटसाठी कोणता BIS मानक लागू आहे?", "mr", "kb-011"),
        ("खेळण्यांसाठी BIS मानक काय आहे?", "mr", "kb-010"),
        ("पॅकेज्ड ड्रिंकिंग वॉटरसाठी कोणता मानक आहे?", "mr", "kb-001"),
        # Kannada
        ("ಸಿಮೆಂಟ್ಗಾಗಿ BIS ಮಾನದಂಡವೇನು?", "kn", "kb-011"),
        ("ಆಟಿಕೆಗಳಿಗೆ BIS ಮಾನದಂಡವೇನು?", "kn", "kb-010"),
        ("ಕುಡಿಯುವ ನೀರಿಗಾಗಿ BIS ಮಾನದಂಡವೇನು?", "kn", "kb-001"),
        # Telugu
        ("సిమెంట్ కోసం BIS ప్రమాణం ఏమిటి?", "te", "kb-011"),
        ("బొమ్మలకు BIS ప్రమాణం ఏమిటి?", "te", "kb-010"),
        ("త్రాగు నీరు కోసం BIS ప్రమాణం ఏమిటి?", "te", "kb-001"),
        # Tamil
        ("சிமெண்டிற்கான BIS தரநிலை என்ன?", "ta", "kb-011"),
        ("பொம்மைகளுக்கான BIS தரநிலை என்ன?", "ta", "kb-010"),
        ("குடிநீருக்கான BIS தரநிலை என்ன?", "ta", "kb-001"),
        # Gujarati
        ("સિમેન્ટ માટે BIS ધોરણ શું છે?", "gu", "kb-011"),
        ("રમકડાં માટે BIS ધોરણ શું છે?", "gu", "kb-010"),
        ("પીવાના પાણી માટે BIS ધોરણ શું છે?", "gu", "kb-001")
    ]

    for query, lang, expected_id in cases:
        result = find_standard_for_product(query, language=lang)
        assert result is not None, f"Query '{query}' returned None"
        assert result["sources"][0]["id"] == expected_id, f"Query '{query}' mismatched"

def test_english_paraphrases():
    cases = [
        ("drinking water testing", "kb-001"),
        ("toy safety testing", "kb-010")
    ]

    for query, expected_id in cases:
        result = find_standard_for_product(query, language="en")
        assert result is not None, f"Query '{query}' returned None"
        assert result["sources"][0]["id"] == expected_id, f"Query '{query}' mismatched"

def test_unsupported_adversarial_queries():
    cases = [
        ("aircraft certification", "en"),
        ("flying car certification", "en"),
        ("विमानासाठी प्रमाणपत्र आवश्यक आहे का?", "mr"), # Aircraft certification in Marathi
        ("विमान प्रमाणन", "hi") # Aircraft certification in Hindi
    ]

    for query, lang in cases:
        result = find_standard_for_product(query, language=lang)
        assert result is None, f"Adversarial query '{query}' incorrectly matched {result['sources'][0]['id'] if result else None}"

def test_generic_service_queries():
    cases = [
        "certification",
        "testing",
        "requirements",
        "BIS",
        "BIS standard",
        "BIS certification",
        "where is the laboratory",
        "how to apply"
    ]

    for query in cases:
        result = find_standard_for_product(query, language="en")
        assert result is None, f"Generic query '{query}' incorrectly matched {result['sources'][0]['id'] if result else None}"

def test_product_plus_service_queries():
    cases = [
        ("How can I get BIS certification for cement?", "kb-011"),
        ("Where can I test packaged drinking water?", "kb-001")
    ]

    for query, expected_id in cases:
        result = find_standard_for_product(query, language="en")
        assert result is not None, f"Product+service query '{query}' returned None"
        assert result["sources"][0]["id"] == expected_id, f"Query '{query}' mismatched"

def test_exact_is_number():
    cases = [
        ("IS 269", "kb-011"),
        ("IS 14543", "kb-001")
    ]

    for query, expected_id in cases:
        result = find_standard_for_product(query, language="en")
        assert result is not None, f"Exact ID query '{query}' returned None"
        assert result["sources"][0]["id"] in [expected_id, "kb-017"], f"Query '{query}' mismatched"
