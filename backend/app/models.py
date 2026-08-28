from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ============================================================
# EXISTING CHAT MODELS
# ============================================================

class ChatMessageIn(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    language: str = Field(
        default="en",
        description="en | hi | mr"
    )
    history: Optional[List[ChatMessageIn]] = None


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
    description: str
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
    query: str
    mode: str = Field(default="industry")
    language: str = Field(default="en")

class ComplianceResponse(BaseModel):
    match_found: bool = False
    intent: str
    product: str
    applicable_standard: str
    scheme: str
    why_applicable: str
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