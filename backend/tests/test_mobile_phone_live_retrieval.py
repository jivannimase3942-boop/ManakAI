import pytest
from app.rag import answer_query

def test_mobile_phone_live_retrieval_path():
    """
    Ensures that 'mobile phone' correctly resolves to kb-019 natively,
    even without Gemini semantic help, by leveraging strong alias matches.
    """
    res = answer_query("mobile phone", "en")
    assert res["matched_topic"] == "Mobile Phones"
    assert res["standard_number"] == "IS/IEC 62368-1:2023 / IS 13252 (Part 1):2010"
    assert len(res["sources"]) > 0
    assert res["sources"][0]["id"] == "kb-019"

def test_smartphone_live_retrieval_path():
    """
    Ensures that 'smartphone' correctly resolves to kb-019 natively.
    """
    res = answer_query("smartphone", "en")
    assert res["matched_topic"] == "Mobile Phones"
    assert res["standard_number"] == "IS/IEC 62368-1:2023 / IS 13252 (Part 1):2010"
    assert len(res["sources"]) > 0
    assert res["sources"][0]["id"] == "kb-019"

def test_power_bank_live_retrieval_path():
    """
    Ensures that 'power bank' correctly resolves to kb-020 natively.
    """
    res = answer_query("power bank", "en")
    assert res["matched_topic"] == "Power Banks"
    assert res["standard_number"] == "IS/IEC 62368-1:2023 / IS 13252 (Part 1):2010"
    assert len(res["sources"]) > 0
    assert res["sources"][0]["id"] == "kb-020"
