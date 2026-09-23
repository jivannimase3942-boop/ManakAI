import pytest
from app import intent
from app import decision
from app import rag

def test_intent_detection():
    assert intent.detect_intent("Pressure cooker BIS standard") == "STANDARD_DISCOVERY"
    assert intent.detect_intent("Where can testing be done for pressure cooker?") == "TESTING"
    assert intent.detect_intent("Pressure cooker testing laboratory") == "TESTING"
    assert intent.detect_intent("प्रेशर कुकर की जांच कहाँ कराएं?") == "TESTING"
    assert intent.detect_intent("प्रेशर कुकरची चाचणी कुठे करता येईल?") == "TESTING"
    assert intent.detect_intent("Which standard applies to pressure cooker?") == "STANDARD_DISCOVERY"
    assert intent.detect_intent("How do I get BIS certification for pressure cooker?") == "CERTIFICATION"

def test_decision_output_filtering():
    # Test STANDARD_DISCOVERY
    res1 = decision.generate_compliance_response("Pressure cooker BIS standard", language="en")
    assert res1.intent == "STANDARD_DISCOVERY"
    assert "2347" in res1.applicable_standard
    assert res1.match_found == True
    assert len(res1.requirements) == 0
    assert len(res1.certification_steps) == 0
    assert len(res1.testing) == 0

    # Test TESTING
    res2 = decision.generate_compliance_response("Where can testing be done for pressure cooker?", language="en")
    assert res2.intent == "TESTING"
    assert "2347" in res2.applicable_standard
    assert len(res2.requirements) == 0
    assert len(res2.certification_steps) == 0

def test_negative_flying_cars():
    res3 = decision.generate_compliance_response("Where can testing be done for flying cars?", language="en")
    assert res3.match_found == False
    assert "2347" not in res3.applicable_standard
