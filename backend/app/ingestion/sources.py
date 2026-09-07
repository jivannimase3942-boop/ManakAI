from urllib.parse import urlparse

# Explicit registry of approved official sources
APPROVED_SOURCES = {
    "bis_official": {
        "domain": "www.bis.gov.in",
        "name": "Bureau of Indian Standards",
        "type": "official",
        "enabled": True
    },
    "bis_services": {
        "domain": "services.bis.gov.in",
        "name": "BIS Services Portal",
        "type": "official",
        "enabled": True
    },
    "bis_standards": {
        "domain": "standards.bis.gov.in",
        "name": "BIS Standards Portal",
        "type": "official",
        "enabled": True
    },
    "test_mock": {
        "domain": "mock.local",
        "name": "Mock Test Source",
        "type": "test",
        "enabled": True
    }
}

def validate_source_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www.") and "mock.local" not in domain:
            # handle www prefix consistently if needed, but let's just exact match or suffix match
            pass
            
        for source_id, data in APPROVED_SOURCES.items():
            if data["enabled"] and domain == data["domain"]:
                return True
        return False
    except Exception:
        return False

def get_source_metadata(url: str) -> dict:
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        for source_id, data in APPROVED_SOURCES.items():
            if data["enabled"] and domain == data["domain"]:
                return data
    except Exception:
        pass
    return {}
