import pytest
from app.rag import answer_query
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def extract_id(result):
    if not result or not result.get("sources"):
        return None
    return result["sources"][0]["id"]

# =====================================================================
# CORE 25 PRODUCT TESTS
# =====================================================================

# ------------------------------------
# PRODUCT 1 — PRESSURE COOKER (kb-014)
# ------------------------------------
def test_pc_01():
    res = answer_query("What is IS 2347?", "en")
    assert extract_id(res) == "kb-014"

def test_pc_02():
    res = answer_query("How can I get BIS certification for a pressure cooker?", "en")
    assert extract_id(res) == "kb-014"

def test_pc_03():
    res = answer_query("Where can pressure cooker testing be done?", "en")
    assert extract_id(res) == "kb-014"

def test_pc_04():
    res = answer_query("IS 2347 certification process", "en")
    assert extract_id(res) == "kb-014"

def test_pc_05():
    res = answer_query("प्रेशर कुकरसाठी BIS मानक कोणते आहे?", "mr")
    assert extract_id(res) == "kb-014"

# ------------------------------------
# PRODUCT 2 — MOBILE PHONE (kb-019)
# ------------------------------------
def test_mp_01():
    res = answer_query("What BIS standard applies to mobile phones?", "en")
    assert extract_id(res) == "kb-019"

def test_mp_02():
    res = answer_query("mobile phone BIS standard", "en")
    assert extract_id(res) == "kb-019"

def test_mp_03():
    res = answer_query("smartphone BIS standard", "en")
    assert extract_id(res) == "kb-019"

def test_mp_04():
    res = answer_query("मोबाइल फोन के लिए BIS मानक क्या है?", "hi")
    assert extract_id(res) == "kb-019"

def test_mp_05():
    res = answer_query("मोबाईल फोनसाठी BIS मानक कोणते आहे?", "mr")
    assert extract_id(res) == "kb-019"

# ------------------------------------
# PRODUCT 3 — POWER BANK (kb-020)
# ------------------------------------
def test_pb_01():
    res = answer_query("What BIS standard applies to power banks?", "en")
    assert extract_id(res) == "kb-020"

def test_pb_02():
    res = answer_query("power bank BIS standard", "en")
    assert extract_id(res) == "kb-020"

def test_pb_03():
    res = answer_query("portable power bank BIS", "en")
    assert extract_id(res) == "kb-020"

def test_pb_04():
    res = answer_query("पावर बैंक के लिए BIS मानक क्या है?", "hi")
    assert extract_id(res) == "kb-020"

def test_pb_05():
    res = answer_query("पॉवर बँकसाठी BIS मानक कोणते आहे?", "mr")
    assert extract_id(res) == "kb-020"

# ------------------------------------
# PRODUCT 4 — LED BULB / LAMP (kb-021)
# ------------------------------------
def test_led_01():
    res = answer_query("What BIS standard applies to LED bulbs?", "en")
    assert extract_id(res) == "kb-021"

def test_led_02():
    res = answer_query("LED bulb BIS standard", "en")
    assert extract_id(res) == "kb-021"

def test_led_03():
    res = answer_query("LED lamp BIS certification", "en")
    assert extract_id(res) == "kb-021"

def test_led_04():
    res = answer_query("एलईडी बल्ब के लिए BIS मानक क्या है?", "hi")
    assert extract_id(res) == "kb-021"

def test_led_05():
    res = answer_query("एलईडी बल्बसाठी BIS मानक कोणते आहे?", "mr")
    assert extract_id(res) == "kb-021"

# ------------------------------------
# PRODUCT 5 — ELECTRIC CEILING FAN (kb-026)
# ------------------------------------
def test_fan_01():
    res = answer_query("What BIS standard applies to ceiling fans?", "en")
    assert extract_id(res) == "kb-026"

def test_fan_02():
    res = answer_query("electric ceiling fan BIS compliance", "en")
    assert extract_id(res) == "kb-026"

def test_fan_03():
    res = answer_query("I manufacture electric ceiling fans, what BIS compliance do I need?", "en")
    assert extract_id(res) == "kb-026"

def test_fan_04():
    res = answer_query("सीलिंग फैन के लिए BIS मानक क्या है?", "hi")
    assert extract_id(res) == "kb-026"

def test_fan_05():
    res = answer_query("इलेक्ट्रिक सीलिंग फॅनसाठी BIS मानक कोणते आहे?", "mr")
    assert extract_id(res) == "kb-026"


# =====================================================================
# ADDITIONAL TESTS
# =====================================================================

def test_safety_negatives():
    cases = [
        "where is the laboratory",
        "where are BIS laboratories",
        "tell me about laboratories",
        "where can testing be done",
        "how to apply",
        "flying car BIS certification",
        "IS 999999",
        "quantum toaster BIS standard"
    ]
    for q in cases:
        res = answer_query(q, "en")
        assert extract_id(res) is None
        ans_lower = res.get("answer", "").lower()
        assert "manakai currently provides guidance related to bis standards" in ans_lower or "no verified match" in ans_lower or "i couldn't find a verified match" in ans_lower

def test_service_context_queries():
    assert extract_id(answer_query("testing laboratory for pressure cooker", "en")) == "kb-014"
    assert extract_id(answer_query("where is IS 2347 tested", "en")) == "kb-014"
    assert extract_id(answer_query("laboratory for my pressure cooker", "en")) == "kb-014"

    # But generic should fail
    assert extract_id(answer_query("laboratory", "en")) is None
    assert extract_id(answer_query("testing", "en")) is None

def test_msme_copilot_generic():
    res = client.post("/api/assistant/query", json={"query": "I am an MSME, what should I do?", "language": "en", "mode": "industry"})
    assert res.status_code == 200
    assert "kb-" not in str(res.json().get("sources", []))

    res = client.post("/api/assistant/query", json={"query": "I am an MSME manufacturer, how do I apply?", "language": "en", "mode": "industry"})
    assert res.status_code == 200
    assert "kb-" not in str(res.json().get("sources", []))

def test_collision():
    assert extract_id(answer_query("mobile phone", "en")) == "kb-019"
    assert extract_id(answer_query("smartphone", "en")) == "kb-019"
    assert extract_id(answer_query("power bank", "en")) == "kb-020"
    assert extract_id(answer_query("portable power bank", "en")) == "kb-020"
    assert extract_id(answer_query("mobile phone BIS standard", "en")) == "kb-019"
    assert extract_id(answer_query("power bank BIS standard", "en")) == "kb-020"
