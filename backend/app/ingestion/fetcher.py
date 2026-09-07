import requests
from typing import Optional, Dict
from .sources import validate_source_url

def fetch_content(url: str, timeout: int = 10) -> Optional[str]:
    if not validate_source_url(url):
        raise ValueError(f"Unauthorized source URL: {url}")
        
    # For mock test sources, we can intercept and return a local fixture
    if "mock.local" in url:
        return _get_mock_html(url)
        
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch content from {url}: {e}")

def _get_mock_html(url: str) -> str:
    # A simple deterministic mock fixture for tests
    if "valid_standard" in url:
        return """
        <html>
            <head><title>IS 12345 : Packaged Space Water</title></head>
            <body>
                <h1 class="standard-title">Packaged Space Water</h1>
                <p class="summary">This standard applies to water for space travel.</p>
                <div class="requirements">
                    <ul>
                        <li>Zero gravity packaging</li>
                        <li>Radiation resistance</li>
                    </ul>
                </div>
            </body>
        </html>
        """
    elif "service_record" in url:
        return """
        <html>
            <head><title>BIS Lab Services</title></head>
            <body>
                <h1 class="standard-title">Lab Testing Portal</h1>
                <p class="summary">Portal for booking lab tests.</p>
            </body>
        </html>
        """
    elif "missing_fields" in url:
        return """
        <html>
            <body>
                <p>Nothing useful here.</p>
            </body>
        </html>
        """
    return "<html></html>"
