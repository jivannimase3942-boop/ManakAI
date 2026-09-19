import pytest
from unittest.mock import patch
from app.rag import answer_query
import app.hybrid_retriever
from app.decision import generate_compliance_response

@pytest.fixture(autouse=True)
def mock_sem(monkeypatch):
    def fake_sem(query, *args, **kwargs):
        q = query.lower()
        if "पाण्याची बाटली" in q: return [{"record_id": "kb-001", "similarity": 0.85}]
        if "पाणी" in q: return [{"record_id": "kb-001", "similarity": 0.85}]
        return []
    monkeypatch.setattr(app.hybrid_retriever, "get_semantic_candidates", fake_sem)


def test_multilingual_product_is2347():
    """Test retrieving Pressure Cooker (IS 2347) in EN, HI, MR"""
    # English
    res_en = answer_query("What is the standard for pressure cooker?", "en")
    assert res_en["confidence"] != "none"
    assert "IS 2347" in res_en["standard_number"]
    assert len(res_en["sources"]) > 0
    assert res_en["sources"][0]["verified"] is True

    # Hindi
    res_hi = answer_query("प्रेशर कुकर के लिए मानक क्या है?", "hi")
    assert res_hi["confidence"] != "none"
    assert "IS 2347" in res_hi["standard_number"]
    assert "प्रेशर कुकर" in res_hi["answer"]

    # Marathi
    res_mr = answer_query("प्रेशर कुकरसाठी कोणते मानक लागू आहे?", "mr")
    assert res_mr["confidence"] != "none"
    assert "IS 2347" in res_mr["standard_number"]
    assert "प्रेशर कुकर" in res_mr["answer"]

def test_multilingual_generic_complaint():
    """Test generic complaint queries in HI, MR"""
    # Hindi complaint
    res_hi = answer_query("उपभोक्ता शिकायत कैसे दर्ज करें", "hi")
    assert res_hi["confidence"] != "none"
    assert "उपभोक्ता शिकायतें" in res_hi["matched_topic"] or "Consumer Services" in res_hi["matched_topic"] or "Consumer Complaints" in res_hi.get("answer", "") or "उपभोक्ता शिकायतें" in res_hi.get("answer", "")

    # Marathi complaint
    res_mr = answer_query("ग्राहक तक्रार कशी नोंदवावी", "mr")
    assert res_mr["confidence"] != "none"
    assert "ग्राहक तक्रारी" in res_mr["matched_topic"] or "Consumer Services" in res_mr["matched_topic"] or "Consumer Complaints" in res_mr.get("answer", "") or "ग्राहक तक्रारी" in res_mr.get("answer", "")

def test_multilingual_laboratory_query():
    """Test generic laboratory testing queries in HI, MR"""
    res_hi = answer_query("क्या मैं किसी लैब में प्रेशर कुकर का परीक्षण करवा सकता हूं?", "hi")
    assert res_hi["confidence"] != "none"
    assert "प्रेशर कुकर" in res_hi.get("answer", "").lower() or "testing" in res_hi["matched_topic"].lower() or "is 2347" in res_hi["standard_number"].lower()

    res_mr = answer_query("मी प्रयोगशाळेत प्रेशर कुकरची चाचणी करू शकतो का?", "mr")
    assert res_mr["confidence"] != "none"
    assert "प्रेशर कुकर" in res_mr.get("answer", "").lower() or "चाचणी" in res_mr.get("answer", "").lower() or "testing" in res_mr["matched_topic"].lower() or "is 2347" in res_mr["standard_number"].lower()

def test_localized_aliases():
    """Test using localized aliases directly"""
    # "पानी की बोतल" is a Hindi alias for Packaged Drinking Water
    res_hi = answer_query("पानी की बोतल का नियम", "hi")
    assert res_hi["confidence"] != "none"
    assert "IS 14543" in res_hi["standard_number"] or "Packaged Drinking Water" in res_hi["matched_topic"]

    # "पाण्याची बाटली" is a Marathi alias
    res_mr = answer_query("पाण्याची बाटली नियम", "mr")
    assert res_mr["confidence"] != "none"
    assert "IS 14543" in res_mr["standard_number"] or "Packaged Drinking Water" in res_mr["matched_topic"]

def test_multilingual_compliance_response():
    """Test decision.generate_compliance_response for correct localization of user-facing fields"""

    # English
    res_en = generate_compliance_response("What is the standard for pressure cooker?", mode="industry", language="en")
    assert res_en.match_found is True
    assert "IS 2347" in res_en.applicable_standard
    assert res_en.compliance_status[0] == "✓ Product identified"
    assert "Domestic Pressure Cookers - Specification" in res_en.product

    # Hindi
    res_hi = generate_compliance_response("मुझे प्रेशर कुकर बनाना है। इसके लिए कौन सा BIS मानक लागू है?", mode="industry", language="hi")
    assert res_hi.match_found is True
    assert "IS 2347" in res_hi.applicable_standard
    assert "✓ उत्पाद की पहचान की गई" in res_hi.compliance_status[0]
    assert "प्रेशर कुकर" in res_hi.product

    # Marathi
    res_mr = generate_compliance_response("मला प्रेशर कुकर बनवायचा आहे. त्यासाठी कोणता BIS मानक लागू आहे?", mode="industry", language="mr")
    assert res_mr.match_found is True
    assert "IS 2347" in res_mr.applicable_standard
    assert "✓ उत्पादनाची ओळख झाली" in res_mr.compliance_status[0]
    assert "प्रेशर कुकर" in res_mr.product

    # Unsupported query (Flying Car)
    res_fail = generate_compliance_response("flying car standard", mode="industry", language="en")
    assert res_fail.match_found is False
    assert "No verified match" in res_fail.compliance_status[0]

def test_unsupported_product():
    """Test an unsupported product gracefully falls back to NO VERIFIED MATCH in all languages"""
    res_en = answer_query("flying car standard", "en")
    assert res_en["confidence"] == "none"
    assert "NO VERIFIED MATCH" in res_en["answer"].upper() or "I COULDN'T FIND A VERIFIED MATCH" in res_en["answer"].upper()

    res_hi = answer_query("उड़ने वाली कार मानक", "hi")
    assert res_hi["confidence"] == "none"
    assert "मुझे ManakAI डेमो नॉलेज बेस में इसके लिए कोई सत्यापित जानकारी नहीं मिली" in res_hi["answer"] or "कोई सत्यापित जानकारी नहीं" in res_hi["answer"]

    res_mr = answer_query("उडणारी कार मानक", "mr")
    assert res_mr["confidence"] == "none"
    assert "सत्यापित माहिती सापडली नाही" in res_mr["answer"]

def test_adversarial_product():
    """Test adversarial product testing correctly rejects if product not verified"""
    res_mr = answer_query("रँडम उत्पादनाची चाचणी", "mr")  # Random product testing
    assert res_mr["confidence"] == "none"

def test_canonical_evidence_preservation():
    """Test that canonical evidence is preserved even when localized answers are returned"""
    res_hi = answer_query("प्रेशर कुकर मानक", "hi")
    assert len(res_hi["sources"]) > 0
    source = res_hi["sources"][0]

    # Source metadata must remain the canonical source of truth (i.e. URL must be intact)
    assert source["verified"] is True
    assert "bis.gov.in" in source["source_url"]
