import pytest
from app.rag import find_standard_for_product

def test_english_queries():
    cases = [
        ("mobile phone", "kb-019"),
        ("smartphone BIS", "kb-019"),
        ("power bank", "kb-020"),
        ("LED bulb", "kb-021"),
        ("PVC pipe", "kb-022"),
        ("plywood", "kb-023"),
        ("safety footwear", "kb-024"),
        ("split AC", "kb-025"),
        ("ceiling fan", "kb-026")
    ]
    for query, expected_id in cases:
        record = find_standard_for_product(query, language="en")
        assert record is not None, f"Query '{query}' returned None"
        assert record["sources"][0]["id"] == expected_id, f"Query '{query}' returned {record['sources'][0]['id']} instead of {expected_id}"

def test_hindi_queries():
    cases = [
        ("मोबाइल फोन", "kb-019"),
        ("पावर बैंक", "kb-020"),
        ("एलईडी बल्ब", "kb-021"),
        ("पीवीसी पाइप", "kb-022"),
        ("प्लायवुड", "kb-023"),
        ("सेफ्टी जूते", "kb-024"),
        ("एसी", "kb-025"),
        ("सीलिंग फैन", "kb-026")
    ]
    for query, expected_id in cases:
        record = find_standard_for_product(query, language="hi")
        assert record is not None, f"Query '{query}' returned None"
        assert record["sources"][0]["id"] == expected_id, f"Query '{query}' returned {record['sources'][0]['id']} instead of {expected_id}"

def test_marathi_queries():
    cases = [
        ("मोबाईल", "kb-019"),
        ("पॉवर बँक", "kb-020"),
        ("एलईडी दिवा", "kb-021"),
        ("पीव्हीसी पाइप", "kb-022"),
        ("प्लायवुड", "kb-023"),
        ("सुरक्षा पादत्राणे", "kb-024"),
        ("वातानुकूलक", "kb-025"),
        ("सीलिंग फॅन", "kb-026")
    ]
    for query, expected_id in cases:
        record = find_standard_for_product(query, language="mr")
        assert record is not None, f"Query '{query}' returned None"
        assert record["sources"][0]["id"] == expected_id, f"Query '{query}' returned {record['sources'][0]['id']} instead of {expected_id}"

def test_negative_queries():
    cases = ["flying car", "random unrelated query"]
    for query in cases:
        record = find_standard_for_product(query, language="en")
        assert record is None, f"Query '{query}' unexpectedly returned a match"

def test_collision_resolution():
    # Both use IS 13252 (Part 1):2010 but should resolve strictly based on product scope/aliases
    mobile_record = find_standard_for_product("mobile phone", language="en")
    power_bank_record = find_standard_for_product("power bank", language="en")

    assert mobile_record is not None
    assert power_bank_record is not None

    assert mobile_record["sources"][0]["id"] == "kb-019"
    assert power_bank_record["sources"][0]["id"] == "kb-020"

    assert mobile_record["title"] == "Mobile / Smartphones"
    assert power_bank_record["title"] == "Power Banks"
