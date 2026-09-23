import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app, rate_limits, RATE_LIMIT_REQUESTS

client = TestClient(app)

def test_cors_allowed_origin():
    response = client.options("/api/assistant/query", headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"

def test_cors_rejected_origin():
    response = client.options("/api/assistant/query", headers={"Origin": "http://malicious.com", "Access-Control-Request-Method": "POST"})
    assert "access-control-allow-origin" not in response.headers

def test_security_headers():
    response = client.get("/api/health")
    assert response.headers.get("x-content-type-options") == "nosniff"
    assert response.headers.get("x-frame-options") == "DENY"
    assert response.headers.get("referrer-policy") == "strict-origin-when-cross-origin"

def test_oversized_query():
    long_query = "A" * 501
    response = client.post("/api/assistant/query", json={"query": long_query, "language": "en"})
    assert response.status_code == 422
    assert "Invalid request input" in response.json()["detail"]

def test_oversized_history():
    history = [{"role": "user", "content": "hello"}] * 16
    response = client.post("/api/assistant/query", json={"query": "test", "history": history})
    assert response.status_code == 422

def test_oversized_history_message():
    history = [{"role": "user", "content": "A" * 501}]
    response = client.post("/api/assistant/query", json={"query": "test", "history": history})
    assert response.status_code == 422

def test_malformed_json():
    response = client.post("/api/assistant/query", data="invalid json")
    assert response.status_code == 422
    assert "Invalid request input" in response.json()["detail"]

def test_rate_limiting():
    rate_limits.clear()
    for _ in range(RATE_LIMIT_REQUESTS):
        res = client.post("/api/standard-search", json={"description": "test"})
        assert res.status_code == 200
    res_429 = client.post("/api/standard-search", json={"description": "test"})
    assert res_429.status_code == 429
    assert "Too many requests" in res_429.json()["detail"]
    rate_limits.clear()

def test_context_isolation():
    res1 = client.post("/api/assistant/query", json={"query": "Where is its testing done?", "language": "en"})
    assert "I COULDN'T FIND A VERIFIED MATCH" in res1.json()["answer"].upper() or "NO VERIFIED MATCH" in res1.json()["answer"].upper()

    history = [{"role": "user", "content": "pressure cooker"}, {"role": "assistant", "content": "IS 2347"}]
    res2 = client.post("/api/assistant/query", json={"query": "Where is its testing done?", "history": history, "language": "en"})
    assert "I COULDN'T FIND A VERIFIED MATCH" in res2.json()["answer"].upper() or "NO VERIFIED MATCH" in res2.json()["answer"].upper()

def test_voice_request_validation():
    long_transcript = "B" * 600
    response = client.post("/api/assistant/query", json={"query": long_transcript})
    assert response.status_code == 422
