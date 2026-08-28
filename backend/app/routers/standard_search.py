from fastapi import APIRouter
from ..models import StandardSearchRequest, ComplianceResponse
from .. import decision

router = APIRouter()

@router.post("/api/standard-search", response_model=ComplianceResponse)
def standard_search(req: StandardSearchRequest):
    result = decision.generate_compliance_response(req.description, "industry", req.language)
    return result
