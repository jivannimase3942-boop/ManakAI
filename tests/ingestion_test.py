import pytest
import requests
from unittest.mock import Mock, patch

from src.ingestion import fetch_bis_only, get_source_url


@pytest.fixture
def mock_url():
    return "https://bis.com/data"


@patch("src.ingestion.requests.get")
def test_success(mock_get):
    response = Mock()
    response.text = "BIS data"
    response.status_code = 200
    mock_get.return_value = response

    url = "https://bis.com/data"

    result = fetch_bis_only(url)

    assert isinstance(result, str)
    assert result == "BIS data"
    assert get_source_url(url) == url

    mock_get.assert_called_once_with(url, timeout=5)


@patch("src.ingestion.requests.get")
def test_http_failure(mock_get):
    response = Mock()
    response.status_code = 404

    error = requests.exceptions.HTTPError(response=response)
    response.raise_for_status.side_effect = error

    mock_get.return_value = response

    url = "https://bis.com/invalid"

    with pytest.raises(ValueError) as exc:
        fetch_bis_only(url)

    assert "HTTP error 404" in str(exc.value)


@patch("src.ingestion.requests.get")
def test_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout()

    with pytest.raises(ValueError) as exc:
        fetch_bis_only("https://bis.com/timeout")

    assert "HTTP request timed out" in str(exc.value)


@patch("src.ingestion.requests.get")
def test_empty_response(mock_get):
    response = Mock()
    response.text = ""
    response.status_code = 200
    mock_get.return_value = response

    with pytest.raises(ValueError) as exc:
        fetch_bis_only("https://bis.com/empty")

    assert "Empty response" in str(exc.value)


def test_non_bis_url():
    url = "https://example.com/invalid"

    with pytest.raises(ValueError) as exc:
        fetch_bis_only(url)

    assert "Non-BIS URL" in str(exc.value)


def test_source_url_provenance():
    url = "https://bis.com/data/123"

    assert get_source_url(url) == url
