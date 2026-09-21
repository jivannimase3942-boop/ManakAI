import pytest
from unittest.mock import patch
from app.rag import answer_query

@patch('app.rag.llm.generate', return_value="Mock LLM response")
@patch('app.rag.llm.is_llm_configured', return_value=True)
def test_lpg_cylinder_regression(mock_conf, mock_gen):
    queries = ["LPG cylinder", "LPG cylinders", "gas cylinder"]
    for q in queries:
        res = answer_query(q, "en")
        assert res["standard_number"] == "IS 3196", f"Failed for '{q}', got {res.get('standard_number')}"

@patch('app.rag.llm.generate', return_value="Mock LLM response")
@patch('app.rag.llm.is_llm_configured', return_value=True)
def test_laptop_regression(mock_conf, mock_gen):
    queries = ["laptop", "laptops", "laptop BIS standard", "standard for laptop"]
    for q in queries:
        res = answer_query(q, "en")
        assert res["standard_number"] == "IS 13252 Part 1:2010", f"Failed for '{q}', got {res.get('standard_number')}"

@patch('app.rag.llm.generate', return_value="Mock LLM response")
@patch('app.rag.llm.is_llm_configured', return_value=True)
def test_other_products_regression(mock_conf, mock_gen):
    test_cases = [
        ("mobile phone", "IS/IEC 62368-1:2023 / IS 13252 (Part 1):2010"),
        ("smartphone", "IS/IEC 62368-1:2023 / IS 13252 (Part 1):2010"),
        ("power bank", "IS/IEC 62368-1:2023 / IS 13252 (Part 1):2010"),
        ("packaged drinking water", "IS 14543:2024"),
        ("cement", "IS 269:2015"),
        ("toys", "IS 9873 Part 1:2019"),
        ("protective helmet", "IS 4151:2015"),
        ("pressure cooker", "IS 2347:2017"),
        ("steel rebar", "IS 1786:2008")
    ]
    for q, standard in test_cases:
        res = answer_query(q, "en")
        assert res["standard_number"] == standard, f"Failed for '{q}', got {res.get('standard_number')}"

@patch('app.rag.llm.generate', return_value="Mock LLM response")
@patch('app.rag.llm.is_llm_configured', return_value=True)
def test_invalid_products_regression(mock_conf, mock_gen):
    invalid_queries = [
        "aircraft certification",
        "flying car certification",
        "xyz product certification",
        "random product testing",
        "IS 2690"
    ]
    for q in invalid_queries:
        res = answer_query(q, "en")
        if res.get("standard_number"):
            assert res["standard_number"] != "IS 269", f"Query '{q}' resolved to IS 269!"
        assert res.get("confidence") == "none" or res.get("matched_topic") is None

@patch('app.rag.llm.generate', return_value="Mock LLM response")
@patch('app.rag.llm.is_llm_configured', return_value=True)
def test_multilingual_regression(mock_conf, mock_gen):
    queries = [
        ("LPG cylinder BIS standard", "en", "IS 3196"),
        ("\u090f\u0932\u092a\u0940\u091c\u0940 \u0938\u093f\u0932\u0947\u0902\u0921\u0930 \u0915\u0947 \u0932\u093f\u090f BIS \u092e\u093e\u0928\u0915", "hi", "IS 3196"),
        ("\u090f\u0932\u092a\u0940\u091c\u0940 \u0938\u093f\u0932\u0947\u0902\u0921\u0930\u0938\u093e\u0920\u0940 BIS \u092e\u093e\u0928\u0915", "mr", "IS 3196"),
    ]
    for q, lang, standard in queries:
        res = answer_query(q, lang)
        assert res["standard_number"] == standard, f"Failed for '{q}' ({lang}), got {res.get('standard_number')}"
