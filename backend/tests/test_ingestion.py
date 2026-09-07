import pytest
import os
from app.ingestion.sources import validate_source_url
from app.ingestion.fetcher import fetch_content
from app.ingestion.extractor import extract_metadata
from app.ingestion.normalizer import normalize_to_schema
from app.ingestion.validator import validate_and_store
from app.ingestion.database import Base, engine, SessionLocal, DBIngestionRecord
from app.ingestion.schemas import VerificationStatus
from app import knowledge_base

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_1_valid_approved_source():
    assert validate_source_url("https://www.bis.gov.in/something") == True
    assert validate_source_url("http://mock.local/valid_standard") == True

def test_2_unauthorized_source_blocked():
    assert validate_source_url("https://www.google.com") == False
    with pytest.raises(ValueError):
        fetch_content("https://www.google.com")

def test_3_network_timeout_failure(monkeypatch):
    import requests
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout("Timeout")
    monkeypatch.setattr(requests, "get", mock_get)
    with pytest.raises(RuntimeError):
        fetch_content("https://www.bis.gov.in/timeout")

def test_4_valid_mock_html_extraction():
    html = fetch_content("http://mock.local/valid_standard")
    extracted = extract_metadata(html, "test")
    assert extracted["title"] == "Packaged Space Water"
    assert extracted["standard_number"] == "IS 12345"
    assert len(extracted["requirements"]) == 2

def test_5_missing_fields_not_hallucinated():
    html = fetch_content("http://mock.local/missing_fields")
    extracted = extract_metadata(html, "test")
    assert extracted["title"] is None
    assert extracted["standard_number"] is None
    normalized = normalize_to_schema(extracted, "http://mock.local/missing_fields")
    assert normalized["title"] == ""
    assert normalized["requirements"] == []

def test_6_invalid_record_becomes_rejected():
    html = fetch_content("http://mock.local/missing_fields")
    extracted = extract_metadata(html, "test")
    normalized = normalize_to_schema(extracted, "http://mock.local/missing_fields")
    success, msg, rec = validate_and_store(normalized)
    assert not success
    db = SessionLocal()
    db_rec = db.query(DBIngestionRecord).first()
    assert db_rec.verification_status == VerificationStatus.REJECTED.value
    db.close()

def test_7_valid_record_becomes_pending():
    html = fetch_content("http://mock.local/valid_standard")
    extracted = extract_metadata(html, "test")
    normalized = normalize_to_schema(extracted, "http://mock.local/valid_standard")
    success, msg, rec = validate_and_store(normalized)
    assert success
    assert rec.verification_status == VerificationStatus.PENDING
    db = SessionLocal()
    db_rec = db.query(DBIngestionRecord).first()
    assert db_rec.verification_status == VerificationStatus.PENDING.value
    db.close()

def test_8_pending_record_cannot_appear_in_live_retrieval():
    # Insert a pending record
    html = fetch_content("http://mock.local/valid_standard")
    extracted = extract_metadata(html, "test")
    normalized = normalize_to_schema(extracted, "http://mock.local/valid_standard")
    validate_and_store(normalized)
    
    # Try searching the live system for "Space Water"
    records = knowledge_base.search("Space Water", top_k=3)
    # Since live uses knowledge_base.json and NOT the new sqlite db, it shouldn't be found
    if records:
        assert "Space Water" not in records[0].get("title", "")

def test_9_duplicate_detection():
    html = fetch_content("http://mock.local/valid_standard")
    extracted = extract_metadata(html, "test")
    normalized = normalize_to_schema(extracted, "http://mock.local/valid_standard")
    
    success1, _, _ = validate_and_store(normalized.copy())
    assert success1
    
    # Generate a new ID but exact same standard number & source
    import uuid
    normalized2 = normalized.copy()
    normalized2["id"] = str(uuid.uuid4())
    success2, msg, _ = validate_and_store(normalized2)
    assert not success2
    assert "Duplicate" in msg

def test_10_optional_standard_number_works_for_service_records():
    html = fetch_content("http://mock.local/service_record")
    extracted = extract_metadata(html, "test")
    normalized = normalize_to_schema(extracted, "http://mock.local/service_record")
    success, msg, rec = validate_and_store(normalized)
    assert success
    assert rec.standard_number is None
    assert rec.verification_status == VerificationStatus.PENDING
