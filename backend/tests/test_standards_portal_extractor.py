import pytest
from app.ingestion.extractors.standards_portal import extract_standards_portal_metadata

MOCK_HTML_SPA = """
<!doctype html>
<html lang="en">
<head>
  <title>BIS - Bureau of Indian Standards</title>
</head>
<body>
  <app-root></app-root>
  <script src="main.js"></script>
</body>
</html>
"""

MOCK_HTML_NO_APP_ROOT = """
<html>
    <body>
        <p>No standard metadata found here either.</p>
    </body>
</html>
"""

def test_spa_extraction():
    records = extract_standards_portal_metadata(MOCK_HTML_SPA, "http://mock.url")
    assert len(records) == 0

def test_no_data_extraction():
    records = extract_standards_portal_metadata(MOCK_HTML_NO_APP_ROOT, "http://mock.url")
    assert len(records) == 0
