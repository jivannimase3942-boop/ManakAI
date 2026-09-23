from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_change_impact_unavailable_fallback():
    # Test that a standard with no verified change evidence defaults to UNAVAILABLE
    res = client.post("/api/compliance/impact", json={"standard": "IS 16046", "product": "Batteries"})
    assert res.status_code == 200
    data = res.json()
    assert data["change_status"] == "UNAVAILABLE"
    assert "not have sufficient verified change information" in data["summary"]

def test_change_impact_schema():
    # Test the general schema
    res = client.post("/api/compliance/impact", json={"standard": "IS 13614", "product": "Unknown"})
    assert res.status_code == 200
    data = res.json()
    assert "change_status" in data
    assert "summary" in data
    assert "impact_areas" in data
    assert "affected_users" in data
    assert "recommended_actions" in data
    assert "evidence" in data
    assert "safe" in data
