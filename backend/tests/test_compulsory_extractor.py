import pytest
from app.ingestion.extractors.compulsory import extract_compulsory_products

MOCK_HTML_VALID = """
<html>
    <body>
        <h2>Products under Compulsory Certification</h2>
        <table>
            <tr>
                <th>Sl. No.</th>
                <th>Product / Item</th>
                <th>Indian Standard No.</th>
            </tr>
            <tr>
                <td>1</td>
                <td>Room Air Conditioners</td>
                <td>IS 1391 (Part 1) : 2017</td>
            </tr>
            <tr>
                <td>2</td>
                <td>Packaged Drinking Water</td>
                <td>IS 14543 : 2016</td>
            </tr>
        </table>
    </body>
</html>
"""

MOCK_HTML_NO_TABLES = """
<html>
    <body>
        <p>No tables here.</p>
    </body>
</html>
"""

MOCK_HTML_MALFORMED_HEADERS = """
<html>
    <body>
        <table>
            <tr>
                <th>Unknown Column 1</th>
                <th>Unknown Column 2</th>
            </tr>
            <tr>
                <td>Data 1</td>
                <td>Data 2</td>
            </tr>
        </table>
    </body>
</html>
"""

MOCK_HTML_MISSING_DATA = """
<html>
    <body>
        <table>
            <tr>
                <th>Product</th>
                <th>Indian Standard</th>
            </tr>
            <tr>
                <td>Only Product Name</td>
                <td></td>
            </tr>
            <tr>
                <td></td>
                <td>IS 12345</td>
            </tr>
        </table>
    </body>
</html>
"""

def test_valid_extraction():
    records = extract_compulsory_products(MOCK_HTML_VALID, "http://mock.url")
    assert len(records) == 2
    assert records[0]["title"] == "Room Air Conditioners"
    assert records[0]["standard_number"] == "IS 1391 (Part 1) : 2017"
    assert records[0]["scheme"] == "Scheme-I (ISI Mark)"
    assert records[0]["applicability"] == "Mandatory Certification Required"
    assert records[0]["source_url"] == "http://mock.url"

def test_no_tables():
    records = extract_compulsory_products(MOCK_HTML_NO_TABLES, "http://mock.url")
    assert len(records) == 0

def test_malformed_headers():
    records = extract_compulsory_products(MOCK_HTML_MALFORMED_HEADERS, "http://mock.url")
    assert len(records) == 0

def test_missing_data():
    records = extract_compulsory_products(MOCK_HTML_MISSING_DATA, "http://mock.url")
    assert len(records) == 0  # Both rows have incomplete critical data
