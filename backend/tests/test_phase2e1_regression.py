import pytest
from app.rag import find_standard_for_product

def test_hindi_valid_product():
    res = find_standard_for_product("खिलौनों के लिए BIS मानक क्या है?", language="hi")
    assert res is not None
    assert res["sources"][0]["id"] in ["kb-010", "kb-028"]

def test_marathi_valid_product():
    res = find_standard_for_product("सिमेंटसाठी कोणता BIS मानक लागू आहे?", language="mr")
    assert res is not None
    assert res["sources"][0]["id"] in ["kb-011", "kb-017"]

def test_hindi_generic_query():
    res = find_standard_for_product("प्रयोगशाला कहां है?", language="hi")
    assert res is not None
    assert res["sources"][0]["id"] == "kb-004"

def test_marathi_generic_query():
    res = find_standard_for_product("लॅबमध्ये कसे जायचे?", language="mr")
    assert res is not None
    assert res["sources"][0]["id"] == "kb-004"

def test_aircraft_certification_safety():
    res = find_standard_for_product("aircraft certification", language="en")
    assert res is None

def test_flying_car_safety():
    res = find_standard_for_product("flying car certification", language="en")
    assert res is None

def test_random_unknown_safety():
    res = find_standard_for_product("random unknown product", language="en")
    assert res is None

def test_generic_certification_safety():
    res = find_standard_for_product("certification", language="en")
    assert res is None

def test_generic_testing_safety():
    res = find_standard_for_product("testing", language="en")
    assert res is None

def test_generic_requirements_safety():
    res = find_standard_for_product("requirements", language="en")
    assert res is None

def test_drinking_water_testing():
    res = find_standard_for_product("drinking water testing", language="en")
    assert res is not None
    assert res["sources"][0]["id"] == "kb-001"

def test_cement_testing():
    res = find_standard_for_product("cement testing", language="en")
    assert res is not None
    assert res["sources"][0]["id"] in ["kb-011", "kb-017"]
