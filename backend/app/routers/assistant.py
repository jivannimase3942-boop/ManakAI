from fastapi import APIRouter
from ..models import ComplianceQueryRequest, ComplianceResponse
from .. import decision

router = APIRouter()

@router.post("/api/assistant/query", response_model=ComplianceResponse)
def assistant_query(req: ComplianceQueryRequest):
    result = decision.generate_compliance_response(req.query, req.mode, req.language, req.history)
    return result
