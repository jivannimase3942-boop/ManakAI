from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
import json

client = TestClient(app)

def test_analyze_endpoint_no_file():
    response = client.post("/api/analyze-product")
    assert response.status_code == 422 # FastAPI validation error for missing required param

@patch("app.routers.analyze.analyze_file_content")
@patch("app.decision.generate_compliance_response")
def test_analyze_endpoint_success(mock_decision, mock_vision):
    # Mock vision response
    mock_vision.return_value = {
        "product_identification": {
            "name": "Mobile Phone",
            "category": "Electronics",
            "brand": "TestBrand",
            "model": "X1",
            "manufacturer": "TestMfg",
            "confidence": 0.99,
            "evidence": ["Looks like a phone"]
        },
        "attributes": {"voltage": "5V"},
        "identification_status": "identified"
    }

    # Mock decision response
    from app.models import ComplianceResponse
    mock_decision.return_value = ComplianceResponse(
        match_found=True,
        intent="CERTIFICATION",
        product="Mobile Phone",
        applicable_standard="IS 13252",
        scheme="CRS",
        why_applicable="Found it.",
        disclaimer="Demo mode."
    )

    response = client.post("/api/analyze-product", files={"file": ("test.jpg", b"\xff\xd8\xfffake_image_data", "image/jpeg")})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["success"] == True
    assert data["product_identification"]["name"] == "Mobile Phone"
    assert data["match_found"] == True
    assert data["applicable_standard"] == "IS 13252"
