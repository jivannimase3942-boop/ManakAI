import pytest
from unittest.mock import patch, MagicMock
from app import vision

@pytest.fixture
def mock_gemini():
    with patch("app.vision._get_genai") as mock_genai:
        yield mock_genai

@pytest.fixture
def mock_yolo():
    with patch("app.vision.analyze_with_yolo") as mock_y:
        yield mock_y

def test_gemini_success(mock_gemini, mock_yolo):
    # Setup mock Gemini success
    mock_genai_instance = MagicMock()
    mock_gemini.return_value = mock_genai_instance
    with patch("app.vision.analyze_with_gemini") as mock_analyze_gemini:
        mock_analyze_gemini.return_value = {
            "identification_status": "identified",
            "product_identification": {"name": "Test Product"}
        }
        
        res = vision.analyze_file_content(b"fake", "image/jpeg")
        
        # Verify Gemini used and YOLO NOT called
        assert res["identification_status"] == "identified"
        assert res["product_identification"]["name"] == "Test Product"
        mock_yolo.assert_not_called()

def test_gemini_429_yolo_fallback(mock_gemini, mock_yolo):
    # Setup mock Gemini failure (429)
    mock_genai_instance = MagicMock()
    mock_gemini.return_value = mock_genai_instance
    with patch("app.vision.analyze_with_gemini") as mock_analyze_gemini:
        mock_analyze_gemini.side_effect = Exception("429 Quota Exceeded")
        
        # Setup YOLO success
        mock_yolo.return_value = {
            "identification_status": "identified",
            "product_identification": {"name": "YOLO Product"}
        }
        
        res = vision.analyze_file_content(b"fake", "image/jpeg")
        
        # Verify YOLO fallback occurred
        mock_yolo.assert_called_once()
        assert res["identification_status"] == "identified"
        assert res["product_identification"]["name"] == "YOLO Product"
        assert "Gemini fallback triggered" in res.get("error", "")
        assert "429 Quota Exceeded" in res.get("error", "")

def test_gemini_generic_failure_yolo_fallback(mock_gemini, mock_yolo):
    # Setup mock Gemini returns uncertain gracefully
    mock_genai_instance = MagicMock()
    mock_gemini.return_value = mock_genai_instance
    with patch("app.vision.analyze_with_gemini") as mock_analyze_gemini:
        mock_analyze_gemini.return_value = {
            "identification_status": "uncertain",
            "product_identification": {"name": "Not detected"}
        }
        
        # Setup YOLO success
        mock_yolo.return_value = {
            "identification_status": "identified",
            "product_identification": {"name": "YOLO Generic Fallback"}
        }
        
        res = vision.analyze_file_content(b"fake", "image/jpeg")
        
        # Verify YOLO fallback occurred
        mock_yolo.assert_called_once()
        assert res["identification_status"] == "identified"
        assert res["product_identification"]["name"] == "YOLO Generic Fallback"
        assert "Gemini fallback triggered" in res.get("error", "")

def test_yolo_unavailable_safe_failure(mock_gemini, mock_yolo):
    # Setup Gemini failure
    mock_genai_instance = MagicMock()
    mock_gemini.return_value = mock_genai_instance
    with patch("app.vision.analyze_with_gemini") as mock_analyze_gemini:
        mock_analyze_gemini.side_effect = Exception("API down")
        
        # Setup YOLO unavailable (throws error)
        mock_yolo.side_effect = Exception("YOLO model not found")
        
        res = vision.analyze_file_content(b"fake", "image/jpeg")
        
        # Verify safe failure
        assert res["identification_status"] == "failed"
        assert "Both Gemini and YOLO failed" in res["error"]
        assert "API down" in res["error"]
        assert "YOLO model not found" in res["error"]

def test_uncertain_yolo_result_safe_failure(mock_gemini, mock_yolo):
    # Setup Gemini failure
    mock_gemini.return_value = None # Simulating no API key
    
    # Setup YOLO uncertain
    mock_yolo.return_value = {
        "identification_status": "uncertain",
        "product_identification": {"name": "Unknown", "confidence": 0.05}
    }
    
    res = vision.analyze_file_content(b"fake", "image/jpeg")
    
    # Verify safe failure returned from YOLO
    assert res["identification_status"] == "uncertain"
    assert res["product_identification"]["name"] == "Unknown"
