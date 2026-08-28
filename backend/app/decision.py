from typing import Dict, Any, Optional, List
from .models import ComplianceResponse, SourceRef
from . import knowledge_base
from . import intent
from . import llm

DISCLAIMERS = {
    "en": "This is a prototype demonstration for SIH 2026, not an official BIS service. Please verify final requirements with official BIS sources.",
    "hi": "यह SIH 2026 के लिए एक प्रोटोटाइप प्रदर्शन है, आधिकारिक BIS सेवा नहीं। कृपया अंतिम आवश्यकताओं की पुष्टि आधिकारिक BIS स्रोतों से करें।",
    "mr": "हे SIH 2026 साठी एक प्रोटोटाइप प्रात्यक्षिक आहे, अधिकृत BIS सेवा नाही. कृपया अंतिम आवश्यकतांची खातरजमा अधिकृत BIS स्त्रोतांकडून करा.",
}

def generate_compliance_response(query: str, mode: str = "industry", language: str = "en") -> ComplianceResponse:
    detected_intent = intent.detect_intent(query)
    records = knowledge_base.search(query, top_k=1)
    
    if not records:
        return ComplianceResponse(
            match_found=False,
            intent=detected_intent,
            product="Unknown",
            applicable_standard="N/A",
            scheme="N/A",
            why_applicable="I couldn't identify a verified BIS match for this query. Try: product name, intended use, certification question, or standard number.",
            compliance_status=["⚠ No verified match found"],
            requirements=[],
            required_documents=[],
            testing=[],
            certification_steps=[],
            next_actions=[
                "Identify what information is missing.",
                "Check if you can provide a more specific product name or standard number.",
                "Consult official BIS resources for definitive guidance."
            ],
            missing_information=["Verified information for this product/query is currently unavailable."],
            sources=[],
            confidence="none",
            mode="rule_engine",
            disclaimer=DISCLAIMERS.get(language, DISCLAIMERS["en"])
        )
    
    record = records[0]
    confidence = record.get("_retrieval_confidence", "low")
    
    missing = []
    status = ["✓ Product identified"]
    if record.get("standard_number"):
        status.append("✓ Standard identified")
        
    reqs = record.get("requirements", [])
    docs = record.get("required_documents", [])
    testing = record.get("testing", {})
    test_details = testing.get("details", [])
    cert = record.get("certification", {})
    cert_steps = cert.get("steps", [])
    scheme_name = cert.get("scheme", "N/A")
    
    # Intent-aware missing info & status
    if detected_intent == "DOCUMENTS":
        if docs:
            status.append("✓ Document checklist identified")
        else:
            status.append("⚠ Exact document checklist unavailable")
            missing.append("Exact verified document checklist is not available in the current knowledge base.")
            
    elif detected_intent == "TESTING":
        if testing.get("available") and test_details:
            status.append("✓ Testing route identified")
        else:
            status.append("⚠ Current laboratory list requires verification")
            missing.append("Exact product-specific testing parameters are not available in the current verified knowledge base.")
            
    elif detected_intent in ["CERTIFICATION", "LICENSING"]:
        if cert.get("available") and cert_steps:
            status.append("✓ Certification route identified")
        else:
            status.append("⚠ Certification details incomplete")
            missing.append("Specific certification steps are not available in the current verified knowledge base.")
            
    elif detected_intent == "REQUIREMENTS":
        if reqs:
            status.append("✓ Requirement identified")
        else:
            status.append("⚠ Specific requirements unavailable")
            missing.append("Specific requirements are not available in the current verified knowledge base.")
            
    else:
        status.append("ⓘ Official applicability verification recommended")

    if not cert.get("available"):
        scheme_name = "N/A"
        
    # Generate dynamic next actions based on mode & intent
    next_actions = []
    
    if mode == "consumer" or detected_intent in ["CONSUMER_VERIFICATION", "COMPLAINT"]:
        next_actions = [
            "Verify the product's BIS licence / applicable identifier.",
            "Check the relevant BIS verification mechanism (like BIS Care app).",
            "Report suspected non-compliance if necessary."
        ]
    else:
        # Industry mode actions based on intent
        if detected_intent == "DOCUMENTS":
            next_actions = [
                "Check the current BIS application/document checklist.",
                "Prepare the verified documents.",
                "Continue with the applicable BIS application route."
            ]
        elif detected_intent == "TESTING":
            next_actions = [
                "Confirm the applicable standard.",
                "Identify the currently recognised laboratory.",
                "Complete the required testing."
            ]
        elif detected_intent in ["CERTIFICATION", "LICENSING", "SCHEME_IDENTIFICATION"]:
            next_actions = [
                "Confirm certification applicability.",
                "Follow the applicable BIS certification route.",
                "Verify current fees, documents and procedures."
            ]
        else: # STANDARD or GENERAL
            next_actions = [
                f"Confirm that {record.get('standard_number', 'the standard')} applies to the product.",
                "Review the relevant requirements.",
                "Verify current BIS applicability."
            ]
    
    why_applicable = record.get("applicability", "")
    if not why_applicable:
        why_applicable = record.get("summary", "")
        
    used_llm = False
    if llm.is_llm_configured():
        system_prompt = (
            f"You are ManakAI, an SIH 2026 prototype. Summarize why this standard applies based ONLY on the following text. "
            f"Do not hallucinate. Respond in {language}. Keep it under 2 sentences."
        )
        user_prompt = f"Product: {record.get('title')}\nApplicability text: {why_applicable}"
        try:
            llm_text = llm.generate(system_prompt, user_prompt)
            if llm_text:
                why_applicable = llm_text
                used_llm = True
        except Exception:
            pass
            
    source = SourceRef(
        title=record.get("title", ""),
        standard_number=record.get("standard_number", ""),
        source_name=record.get("source_name", ""),
        source_url=record.get("source_url", ""),
        verified=record.get("verified", True)
    )
    
    return ComplianceResponse(
        match_found=True,
        intent=detected_intent,
        product=record.get("title", ""),
        applicable_standard=record.get("standard_number", ""),
        scheme=scheme_name,
        why_applicable=why_applicable,
        compliance_status=status,
        requirements=reqs,
        required_documents=docs,
        testing=test_details,
        certification_steps=cert_steps,
        next_actions=next_actions,
        missing_information=missing,
        sources=[source],
        confidence=confidence,
        mode="llm" if used_llm else "rule_engine",
        disclaimer=DISCLAIMERS.get(language, DISCLAIMERS["en"])
    )
