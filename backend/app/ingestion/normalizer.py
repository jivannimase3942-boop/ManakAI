from typing import Dict, Any
import uuid
from .sources import get_source_metadata

def normalize_to_schema(extracted: Dict[str, Any], url: str) -> Dict[str, Any]:
    source_meta = get_source_metadata(url)
    
    # We must not invent missing fields, leaving them None or empty
    normalized = {
        "id": str(uuid.uuid4()),
        "title": extracted.get("title") or "",
        "standard_number": extracted.get("standard_number"), # None is allowed
        "topic": extracted.get("title") or "Unknown Topic",
        "summary": extracted.get("summary") or "",
        "applicability": "",
        "requirements": extracted.get("requirements") or [],
        "testing_information": {},
        "certification_information": {},
        "required_documents": [],
        "next_actions": [],
        "keywords": [],
        "source_name": source_meta.get("name", "Unknown Source"),
        "source_url": url,
        "source_type": source_meta.get("type", "unknown")
    }
    
    return normalized
