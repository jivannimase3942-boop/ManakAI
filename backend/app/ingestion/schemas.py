from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime
from enum import Enum

class VerificationStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    OFFICIAL_EVIDENCE = "OFFICIAL_EVIDENCE"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"

class IngestionRecord(BaseModel):
    id: str
    title: str
    product_domain: Optional[str] = None
    service_category: Optional[str] = None
    standard_number: Optional[str] = None
    standard_title: Optional[str] = None
    topic: str
    summary: str
    applicability: str
    requirements: List[str] = Field(default_factory=list)
    testing_information: Dict[str, Any] = Field(default_factory=dict)
    certification_information: Dict[str, Any] = Field(default_factory=dict)
    required_documents: List[str] = Field(default_factory=list)
    consumer_actions: List[str] = Field(default_factory=list)
    industry_actions: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    documents: List[Dict[str, Any]] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    source_name: str
    source_url: str
    source_type: str
    verification_status: VerificationStatus = VerificationStatus.PENDING
    source_checked_date: Optional[str] = None
    notes_evidence: Optional[str] = None
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    last_verified: Optional[datetime] = None
    revision: int = 1
    supersedes_id: Optional[str] = None
