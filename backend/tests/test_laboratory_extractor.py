import pytest
from app.ingestion.extractors.laboratory import extract_laboratory_metadata

MOCK_HTML_VALID = """
<html>
    <body>
        <main>
            <h1>Laboratory Recognition Scheme</h1>
            <p>BIS operates a Laboratory Recognition Scheme to ensure that laboratories testing samples are competent.</p>
            <p>We provide testing facilities across India.</p>
            <a href="https://lims.bis.gov.in/home/search_is_number/">LIMS Portal</a>
        </main>
    </body>
</html>
"""

MOCK_HTML_NO_CONTENT = """
<html>
    <body>
        <main>
            <p>Some unrelated text without our keywords.</p>
        </main>
    </body>
</html>
"""

MOCK_HTML_SPA_LIMS = """
<html>
    <body>
        <app-root></app-root>
    </body>
</html>
"""

def test_valid_extraction():
    records = extract_laboratory_metadata(MOCK_HTML_VALID, "http://mock.url")
    assert len(records) == 1
    assert records[0]["title"] == "BIS Laboratory & Testing Information"
    assert records[0]["standard_number"] is None
    assert records[0]["scheme"] == "Laboratory Recognition Scheme / LIMS"
    assert "BIS operates a Laboratory" in records[0]["applicability"]
    assert "Important Links:\\nLIMS Portal: https://lims.bis.gov.in/home/search_is_number/" in records[0]["applicability"]
    assert records[0]["source_url"] == "http://mock.url"

def test_no_content():
    records = extract_laboratory_metadata(MOCK_HTML_NO_CONTENT, "http://mock.url")
    assert len(records) == 0

def test_spa_lims():
    records = extract_laboratory_metadata(MOCK_HTML_SPA_LIMS, "http://mock.url")
    assert len(records) == 0
