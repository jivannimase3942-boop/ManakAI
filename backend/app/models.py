from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ============================================================
# EXISTING CHAT MODELS
# ============================================================

class ChatMessageIn(BaseModel):
    role: str
    content: str = Field(..., max_length=500, min_length=1)


class ChatRequest(BaseModel):
    message: str = Field(..., max_length=500, min_length=1)
    language: str = Field(
        default="en",
        description="en | hi | mr"
    )
    history: Optional[List[ChatMessageIn]] = Field(default=None, max_length=15)


class SourceRef(BaseModel):
    title: str
    standard_number: str = ""
    source_name: str
    source_url: str
    verified: bool = True


class ChatResponse(BaseModel):
    answer: str
    matched_topic: Optional[str] = None
    standard_number: Optional[str] = None
    sources: List[SourceRef] = Field(default_factory=list)
    mode: str = "demo"
    confidence: str = "none"
    disclaimer: str


# ============================================================
# STANDARD FINDER
# ============================================================

class StandardSearchRequest(BaseModel):
    description: str = Field(..., max_length=500, min_length=1)
    language: str = Field(default="en")


class StandardSearchResult(BaseModel):
    title: str
    standard_number: str
    topic: str
    summary: str
    guidance: str
    sources: List[SourceRef] = Field(default_factory=list)
    confidence: str


# ============================================================
# BIS SERVICES
# ============================================================

class ServiceCard(BaseModel):
    id: str
    name: str
    description: str
    icon: str


class SourceListItem(BaseModel):
    title: str
    standard_number: str
    source_name: str
    source_url: str


# ============================================================
# NEW MANAKAI COMPLIANCE ENGINE
# ============================================================

class ComplianceQueryRequest(BaseModel):
    query: str = Field(..., max_length=500, min_length=1)
    mode: str = Field(default="industry")
    language: str = Field(default="en")
    history: Optional[List[ChatMessageIn]] = Field(default=None, max_length=15)


class ComplianceResponse(BaseModel):
    match_found: bool = False
    intent: str
    product: str
    applicable_standard: str
    scheme: str
    why_applicable: str
    answer: str = ""
    why_this_answer: str = ""
    compliance_status: List[str] = Field(default_factory=list)
    requirements: List[str] = Field(default_factory=list)
    required_documents: List[str] = Field(default_factory=list)
    testing: List[str] = Field(default_factory=list)
    certification_steps: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    sources: List[SourceRef] = Field(default_factory=list)
    confidence: str = "none"
    mode: str = "rule_engine"
    disclaimer: str

    # Phase 2F: Structured Fields (Optional for backward compatibility)
    structured_compliance_journey: Optional[Dict[str, Any]] = None
    structured_documents: Optional[List[Dict[str, Any]]] = None
    structured_testing: Optional[Dict[str, Any]] = None
    structured_fees: Optional[Dict[str, Any]] = None
    regulatory_status: Optional[Dict[str, Any]] = None
    official_links: Optional[List[Dict[str, Any]]] = None
    structured_evidence: Optional[List[Dict[str, Any]]] = None


class ComplianceImpactRequest(BaseModel):
    standard: str = Field(..., max_length=100)
    product: Optional[str] = Field(default=None, max_length=200)

class ComplianceImpactResponse(BaseModel):
    standard: str
    product: str
    change_status: str
    summary: str
    impact_areas: List[str] = Field(default_factory=list)
    affected_users: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    evidence: List[SourceRef] = Field(default_factory=list)
    safe: bool = True

from typing import Dict, Any, Optional, List
from pydantic import BaseModel

class ProductIdentification(BaseModel):
    name: str
    category: str
    brand: str
    model: str
    manufacturer: str
    confidence: float
    evidence: List[str]
    status: str

class ProductAnalysisResponse(BaseModel):
    success: bool
    source_type: str
    product_identification: ProductIdentification
    attributes: Dict[str, Any]

    # Nested fields from ComplianceResponse
    match_found: bool = False
    intent: str = ""
    product: str = ""
    applicable_standard: str = ""
    scheme: str = ""
    why_applicable: str = ""
    answer: str = ""
    why_this_answer: str = ""
    compliance_status: List[str] = []
    requirements: List[str] = []
    required_documents: List[str] = []
    testing: List[str] = []
    certification_steps: List[str] = []
    next_actions: List[str] = []
    missing_information: List[str] = []
    sources: List[Any] = []
    confidence: str = "none"
    mode: str = "rule_engine"
    disclaimer: str = ""

    # Structured Phase 2F fields
    structured_compliance_journey: Optional[List[Dict[str, Any]]] = None
    structured_documents: Optional[List[Dict[str, Any]]] = None
    structured_testing: Optional[Dict[str, Any]] = None
    structured_fees: Optional[Dict[str, Any]] = None
    regulatory_status: Optional[Dict[str, Any]] = None
    official_links: Optional[List[Dict[str, Any]]] = None
    structured_evidence: Optional[List[Dict[str, Any]]] = None

    # Specific attributes for partial/no match
    multiple_candidates: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
