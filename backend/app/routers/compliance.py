from fastapi import APIRouter
from ..models import ComplianceImpactRequest, ComplianceImpactResponse, SourceRef
from .. import knowledge_base

router = APIRouter()

@router.post("/api/compliance/impact", response_model=ComplianceImpactResponse)
def get_compliance_impact(req: ComplianceImpactRequest):
    # Retrieve the exact record from the knowledge base by standard number
    records = knowledge_base.search(req.standard, top_k=5)

    # Try to find the exact standard
    target_record = None
    for r in records:
        if r.get("standard_number", "").strip().lower() == req.standard.strip().lower():
            target_record = r
            break

    if not target_record:
        # Fallback to first result if it's highly relevant
        if records:
            target_record = records[0]

    if not target_record:
        return ComplianceImpactResponse(
            standard=req.standard,
            product=req.product or "Unknown Product",
            change_status="UNAVAILABLE",
            summary="ManakAI currently does not have sufficient verified change information to determine the status.",
            impact_areas=[],
            affected_users=[],
            recommended_actions=[],
            evidence=[],
            safe=True
        )

    change_info = target_record.get("change_information", {})
    status = change_info.get("status", "UNAVAILABLE")

    # Evidence gating: If status is VERIFIED_CHANGE but there is no evidence, fallback to UNAVAILABLE
    evidence_list = []
    raw_evidence = change_info.get("evidence", [])
    for e in raw_evidence:
        evidence_list.append(SourceRef(
            title=e.get("title", ""),
            standard_number=e.get("standard_number", req.standard),
            source_name=e.get("source_name", ""),
            source_url=e.get("source_url", ""),
            verified=e.get("verified", True)
        ))

    if status == "VERIFIED_CHANGE" and not evidence_list:
        status = "UNAVAILABLE"

    summary = change_info.get("summary", "")
    if not summary:
        if status == "NO_VERIFIED_CHANGE":
            summary = "No verified change information currently available."
        else:
            summary = "ManakAI currently does not have sufficient verified change information to determine the status."

    return ComplianceImpactResponse(
        standard=target_record.get("standard_number", req.standard),
        product=req.product or target_record.get("title", "Unknown Product"),
        change_status=status,
        summary=summary,
        impact_areas=change_info.get("impact_areas", []),
        affected_users=change_info.get("affected_users", []),
        recommended_actions=change_info.get("recommended_actions", []),
        evidence=evidence_list,
        safe=True
    )
