from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime
from enum import Enum

class VerificationStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"

class IngestionRecord(BaseModel):
    id: str
    title: str
    standard_number: Optional[str] = None
    topic: str
    summary: str
    applicability: str
    requirements: List[str] = Field(default_factory=list)
    testing_information: Dict[str, Any] = Field(default_factory=dict)
    certification_information: Dict[str, Any] = Field(default_factory=dict)
    required_documents: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    source_name: str
    source_url: str
    source_type: str
    verification_status: VerificationStatus = VerificationStatus.PENDING
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    last_verified: Optional[datetime] = None
    revision: int = 1
    supersedes_id: Optional[str] = None
