import requests


# Feature 1A: Official BIS-only fetcher
def fetch_bis_only(url):
    # Validate BIS domain
    if not url.startswith("https://bis.com"):
        raise ValueError("Non-BIS URL")

    try:
        # Safe HTTP handling with timeout
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        if not response.text:
            raise ValueError("Empty response")

        return response.text

    except requests.exceptions.Timeout:
        raise ValueError("HTTP request timed out")

    except requests.exceptions.HTTPError as e:
        raise ValueError(f"HTTP error {e.response.status_code}")


# Source URL preservation
def get_source_url(url):
    return url
