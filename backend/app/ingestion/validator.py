from pydantic import ValidationError
from .schemas import IngestionRecord, VerificationStatus
from .database import SessionLocal, DBIngestionRecord
from typing import Dict, Any, Tuple
import re

def validate_and_store(normalized: Dict[str, Any]) -> Tuple[bool, str, Any]:
    # Custom validation logic
    if not normalized.get("title") or not normalized.get("summary"):
        # We reject records that lack basic necessary fields
        normalized["verification_status"] = VerificationStatus.REJECTED.value
        _save_to_db(normalized)
        return False, "Missing required title or summary", None
        
    std_num = normalized.get("standard_number")
    if std_num:
        # Validate format (e.g. starts with IS)
        if not re.match(r'^IS\s\d+', std_num, re.IGNORECASE):
            normalized["verification_status"] = VerificationStatus.REJECTED.value
            _save_to_db(normalized)
            return False, f"Malformed standard number: {std_num}", None

    try:
        record = IngestionRecord(**normalized)
    except ValidationError as e:
        normalized["verification_status"] = VerificationStatus.REJECTED.value
        _save_to_db(normalized)
        return False, f"Schema validation failed: {e}", None

    # Check for duplicates using source_url and standard_number or title
    db = SessionLocal()
    try:
        query = db.query(DBIngestionRecord).filter(DBIngestionRecord.source_url == record.source_url)
        if record.standard_number:
            query = query.filter(DBIngestionRecord.standard_number == record.standard_number)
        else:
            query = query.filter(DBIngestionRecord.title == record.title)
            
        existing = query.first()
        
        if existing:
            # Duplicate found
            # Could increment revision and link supersedes_id, but for Phase 2A we just reject as duplicate
            record.verification_status = VerificationStatus.REJECTED
            _save_to_db(record.dict())
            return False, "Duplicate record detected from this source.", None
    finally:
        db.close()

    record.verification_status = VerificationStatus.PENDING
    _save_to_db(record.dict())
    return True, "Success", record

def _save_to_db(record_dict: Dict[str, Any]):
    db = SessionLocal()
    try:
        db_record = DBIngestionRecord(**record_dict)
        db.add(db_record)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"DB save error: {e}")
    finally:
        db.close()
