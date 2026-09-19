from typing import Dict, Any, Optional, List
import os
from .models import ComplianceResponse, SourceRef
from .rag import DISCLAIMERS, NO_MATCH_TEXT, LANG_NAMES
from . import knowledge_base
from . import intent
from . import llm
from . import hybrid_retriever
from .models import ChatMessageIn

USE_HYBRID_RETRIEVAL = os.getenv("USE_HYBRID_RETRIEVAL", "true").lower() == "true"

def augment_query_with_history(query: str, history: Optional[List[ChatMessageIn]]) -> str:
    # History context is now strictly handled by the frontend via explicit pronoun resolution.
    # Blindly prepending keywords from history violates the safety bounds and causes context bleed.
    return query

def compose_answer(query: str, intent_name: str, record: dict, language: str) -> Optional[Dict[str, str]]:
    i18n_record = record.get("i18n", {}).get(language)
    if not i18n_record:
        return None

    q_lower = query.lower()

    if intent_name == "TESTING":
        testing = i18n_record.get("testing") or record.get("testing", {})
        details = testing.get("details", [])
        if not details:
            return None

        is_location_query = any(w in q_lower for w in ["where", "कुठे", "कहाँ"])
        details_text = " ".join(details).lower()
        if is_location_query:
            if not any(w in details_text for w in ["lab", "laboratory", "centre", "center", "location", "facility", "प्रयोगशाळा", "प्रयोगशाला", "recognized"]):
                return None

        ans = "\n".join(details)
        if language == "hi":
            why = "इस उत्पाद के लिए सत्यापित परीक्षण जानकारी।"
        elif language == "mr":
            why = "या उत्पादनासाठी सत्यापित चाचणी माहिती."
        else:
            why = "Verified testing information for this product."
        return {"answer": ans, "why_this_answer": why}

    elif intent_name in ["CERTIFICATION", "LICENSING", "SCHEME"]:
        cert = i18n_record.get("certification") or record.get("certification", {})
        steps = cert.get("steps", [])
        scheme = cert.get("scheme", "")
        if not steps and not scheme:
            return None

        lines = []
        if scheme:
            lines.append(f"Scheme: {scheme}")
        if steps:
            lines.append("Process: " + " → ".join(steps))

        if language == "hi":
            why = "इस उत्पाद के लिए सत्यापित प्रमाणन प्रक्रिया।"
        elif language == "mr":
            why = "या उत्पादनासाठी सत्यापित प्रमाणन प्रक्रिया."
        else:
            why = "Verified certification process for this product."
        return {"answer": "\n".join(lines), "why_this_answer": why}

    elif intent_name == "DOCUMENTS":
        docs = i18n_record.get("required_documents") or record.get("required_documents", [])
        if not docs:
            return None

        if language == "hi":
            why = "सत्यापित दस्तावेज़ चेकलिस्ट।"
        elif language == "mr":
            why = "सत्यापित दस्तऐवज चेकलिस्ट."
        else:
            why = "Verified document checklist for this product."
        return {"answer": "\n".join([f"- {d}" for d in docs]), "why_this_answer": why}

    elif intent_name == "REQUIREMENTS":
        reqs = i18n_record.get("requirements") or record.get("requirements", [])
        if not reqs:
            return None

        if language == "hi":
            why = "सत्यापित आवश्यकताएं।"
        elif language == "mr":
            why = "सत्यापित आवश्यकता."
        else:
            why = "Verified requirements for this product."
        return {"answer": "\n".join([f"- {r}" for r in reqs]), "why_this_answer": why}

    elif intent_name == "COMPLAINT":
        consumer = i18n_record.get("consumer_actions") or record.get("consumer_actions", [])
        if not consumer:
            return None

        if language == "hi":
            why = "सत्यापित उपभोक्ता मार्गदर्शन।"
        elif language == "mr":
            why = "सत्यापित ग्राहक मार्गदर्शन."
        else:
            why = "Verified consumer guidance."
        return {"answer": "\n".join([f"- {c}" for c in consumer]), "why_this_answer": why}

    elif intent_name in ["STANDARD_DISCOVERY", "GENERAL_BIS_GUIDANCE"]:
        std = record.get("standard_number", "")
        app = i18n_record.get("applicability") or i18n_record.get("summary") or record.get("applicability") or record.get("summary", "")

        lines = []
        if std:
            lines.append(f"{std}")
        if app:
            lines.append(app)

        if not lines:
            return None

        if language == "hi":
            why = "इस उत्पाद के लिए सत्यापित मानक और प्रयोज्यता।"
        elif language == "mr":
            why = "या उत्पादनासाठी सत्यापित मानक आणि लागू होण्याची शक्यता."
        else:
            why = "Verified standard and applicability for this product."
        return {"answer": "\n".join(lines), "why_this_answer": why}

    return None

def generate_compliance_response(query: str, mode: str = "industry", language: str = "en", history: Optional[List[ChatMessageIn]] = None) -> ComplianceResponse:
    from .rag import _is_bis_scope, SCOPE_REJECT_TEXT

    augmented_query = query

    if not _is_bis_scope(augmented_query):
        return ComplianceResponse(
            match_found=False,
            intent="UNKNOWN",
            product="Unknown",
            applicable_standard="N/A",
            scheme="N/A",
            why_applicable=SCOPE_REJECT_TEXT.get(language, SCOPE_REJECT_TEXT["en"]),
            compliance_status=["❌ Out of Scope"],
            requirements=[],
            required_documents=[],
            testing=[],
            certification_steps=[],
            next_actions=[],
            missing_information=["This query is outside the scope of ManakAI."],
            sources=[],
            confidence="none",
            mode="rule_engine",
            disclaimer=DISCLAIMERS.get(language, DISCLAIMERS["en"])
        )

    detected_intent = intent.detect_intent(augmented_query)

    # CTX-BACKEND Trace
    try:
        print(f"[CTX-BACKEND] received_query={query}")
        print(f"[CTX-BACKEND] history_count={len(history) if history else 0}")
        print(f"[CTX-BACKEND] history_latest={(history[-1].content if history else '')}")
        print(f"[CTX-BACKEND] contextual_resolution=frontend_only")
        print(f"[CTX-BACKEND] effective_query={augmented_query}")
        print(f"[CTX-BACKEND] detected_intent={detected_intent}")
    except Exception:
        pass

    if USE_HYBRID_RETRIEVAL:
        records = hybrid_retriever.hybrid_search(augmented_query, top_k=1)
        if not records:
            is_ascii = all(ord(c) < 128 for c in augmented_query)
            if not is_ascii and llm.is_llm_configured():
                norm_context = llm.extract_query_context(augmented_query)
                if norm_context:
                    records = hybrid_retriever.hybrid_search(augmented_query, top_k=1, norm_context=norm_context)
    else:
        records = knowledge_base.search(augmented_query, top_k=1)

    if not records:
        print(f"[CTX-BACKEND] selected_record=None")
        print(f"[CTX-BACKEND] match_found=False")
        return ComplianceResponse(
            match_found=False,
            intent=detected_intent,
            product="Unknown",
            applicable_standard="N/A",
            scheme="N/A",
            why_applicable=NO_MATCH_TEXT.get(language, NO_MATCH_TEXT["en"]),
            compliance_status=["❌ No verified match found"],
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
            disclaimer=DISCLAIMERS.get(language, DISCLAIMERS["en"]),
            answer=NO_MATCH_TEXT.get(language, NO_MATCH_TEXT["en"]),
            why_this_answer="No matching verified record was found."
        )

    record = records[0]
    print(f"[CTX-BACKEND] selected_record={record.get('id', 'Unknown')}")
    print(f"[CTX-BACKEND] match_found=True")

    # 1. Compose direct answer
    composed = compose_answer(augmented_query, detected_intent, record, language)
    if not composed:
        if detected_intent in ["TESTING", "CERTIFICATION", "LICENSING", "SCHEME", "DOCUMENTS", "REQUIREMENTS", "COMPLAINT"]:
            composed = {
                "answer": NO_MATCH_TEXT.get(language, NO_MATCH_TEXT["en"]),
                "why_this_answer": "The verified record does not contain the requested specific information."
            }
        else:
            composed = {"answer": "", "why_this_answer": ""}
    confidence = record.get("_retrieval_confidence", "low")

    # Extract i18n fields
    i18n_record = record.get("i18n", {}).get(language, record.get("i18n", {}).get("en", {}))
    title = i18n_record.get("title", record.get("title", ""))

    why_applicable = i18n_record.get("applicability")
    if not why_applicable:
        why_applicable = i18n_record.get("summary")
    if not why_applicable:
        why_applicable = record.get("applicability")
    if not why_applicable:
        why_applicable = record.get("summary", "")

    reqs = i18n_record.get("requirements", record.get("requirements", []))
    docs = i18n_record.get("required_documents", record.get("required_documents", []))
    testing = i18n_record.get("testing", record.get("testing", {}))
    testing_available = testing.get("available", record.get("testing", {}).get("available", False))
    test_details = testing.get("details", record.get("testing", {}).get("details", []))

    cert = i18n_record.get("certification", record.get("certification", {}))
    cert_available = cert.get("available", record.get("certification", {}).get("available", False))
    cert_steps = cert.get("steps", record.get("certification", {}).get("steps", []))
    scheme_name = cert.get("scheme", record.get("certification", {}).get("scheme", "N/A"))

    # Intent-aware Response Filtering
    if detected_intent == "TESTING":
        reqs = []
        cert_steps = []
    elif detected_intent == "STANDARD_DISCOVERY":
        test_details = []
        cert_steps = []
        reqs = []
    elif detected_intent in ["CERTIFICATION", "LICENSING", "SCHEME"]:
        test_details = []
    elif detected_intent == "REQUIREMENTS":
        test_details = []
        cert_steps = []

    missing = []

    # Translations for compliance_status and missing
    STATUS_TEXT = {
        "en": {
            "prod_ident": "✓ Product identified",
            "std_ident": "✓ Standard identified",
            "doc_ident": "✓ Document checklist identified",
            "doc_unavail": "⚠ Exact document checklist unavailable",
            "test_ident": "✓ Testing route identified",
            "test_unavail": "⚠ Current laboratory list requires verification",
            "cert_ident": "✓ Certification route identified",
            "cert_unavail": "⚠ Certification details incomplete",
            "req_ident": "✓ Requirement identified",
            "req_unavail": "⚠ Specific requirements unavailable",
            "official_rec": "ⓘ Official applicability verification recommended",

            "miss_doc": "Exact verified document checklist is not available in the current knowledge base.",
            "miss_test": "Exact product-specific testing parameters are not available in the current verified knowledge base.",
            "miss_cert": "Specific certification steps are not available in the current verified knowledge base.",
            "miss_req": "Specific requirements are not available in the current verified knowledge base."
        },
        "hi": {
            "prod_ident": "✓ उत्पाद की पहचान की गई",
            "std_ident": "✓ मानक की पहचान की गई",
            "doc_ident": "✓ दस्तावेज़ चेकलिस्ट की पहचान की गई",
            "doc_unavail": "⚠ सटीक दस्तावेज़ चेकलिस्ट उपलब्ध नहीं है",
            "test_ident": "✓ परीक्षण मार्ग की पहचान की गई",
            "test_unavail": "⚠ वर्तमान प्रयोगशाला सूची के सत्यापन की आवश्यकता है",
            "cert_ident": "✓ प्रमाणन मार्ग की पहचान की गई",
            "cert_unavail": "⚠ प्रमाणन विवरण अधूरा है",
            "req_ident": "✓ आवश्यकता की पहचान की गई",
            "req_unavail": "⚠ विशिष्ट आवश्यकताएं उपलब्ध नहीं हैं",
            "official_rec": "ⓘ आधिकारिक प्रयोज्यता सत्यापन की सिफारिश की जाती है",

            "miss_doc": "वर्तमान सत्यापित ज्ञानकोष में सटीक सत्यापित दस्तावेज़ चेकलिस्ट उपलब्ध नहीं है।",
            "miss_test": "वर्तमान सत्यापित ज्ञानकोष में सटीक उत्पाद-विशिष्ट परीक्षण पैरामीटर उपलब्ध नहीं हैं।",
            "miss_cert": "वर्तमान सत्यापित ज्ञानकोष में विशिष्ट प्रमाणन चरण उपलब्ध नहीं हैं।",
            "miss_req": "वर्तमान सत्यापित ज्ञानकोष में विशिष्ट आवश्यकताएं उपलब्ध नहीं हैं।"
        },
        "mr": {
            "prod_ident": "✓ उत्पादनाची ओळख झाली",
            "std_ident": "✓ मानकाची ओळख झाली",
            "doc_ident": "✓ दस्तऐवज चेकलिस्टची ओळख झाली",
            "doc_unavail": "⚠ अचूक दस्तऐवज चेकलिस्ट अनुपलब्ध आहे",
            "test_ident": "✓ चाचणी मार्गाची ओळख झाली",
            "test_unavail": "⚠ वर्तमान प्रयोगशाळा सूचीच्या पडताळणीची आवश्यकता आहे",
            "cert_ident": "✓ प्रमाणन मार्गाची ओळख झाली",
            "cert_unavail": "⚠ प्रमाणन तपशील अपूर्ण आहे",
            "req_ident": "✓ आवश्यकतेची ओळख झाली",
            "req_unavail": "⚠ विशिष्ट आवश्यकता उपलब्ध नाहीत",
            "official_rec": "ⓘ अधिकृत लागू होण्याच्या पडताळणीची शिफारस केली जाते",

            "miss_doc": "सध्याच्या सत्यापित ज्ञानकोशात अचूक सत्यापित दस्तऐवज चेकलिस्ट उपलब्ध नाही.",
            "miss_test": "सध्याच्या सत्यापित ज्ञानकोशात अचूक उत्पादन-विशिष्ट चाचणी परिमाणे उपलब्ध नाहीत.",
            "miss_cert": "सध्याच्या सत्यापित ज्ञानकोशात विशिष्ट प्रमाणन टप्पे उपलब्ध नाहीत.",
            "miss_req": "सध्याच्या सत्यापित ज्ञानकोशात विशिष्ट आवश्यकता उपलब्ध नाहीत."
        }
    }

    st = STATUS_TEXT.get(language, STATUS_TEXT["en"])

    status = [st["prod_ident"]]
    if record.get("standard_number"):
        status.append(st["std_ident"])

    # Intent-aware missing info & status
    if detected_intent == "DOCUMENTS":
        if docs:
            status.append(st["doc_ident"])
        else:
            status.append(st["doc_unavail"])
            missing.append(st["miss_doc"])

    elif detected_intent == "TESTING":
        if testing_available and test_details:
            status.append(st["test_ident"])
        else:
            status.append(st["test_unavail"])
            missing.append(st["miss_test"])

    elif detected_intent in ["CERTIFICATION", "LICENSING"]:
        if cert_available and cert_steps:
            status.append(st["cert_ident"])
        else:
            status.append(st["cert_unavail"])
            missing.append(st["miss_cert"])

    elif detected_intent == "REQUIREMENTS":
        if reqs:
            status.append(st["req_ident"])
        else:
            status.append(st["req_unavail"])
            missing.append(st["miss_req"])

    elif detected_intent == "MSME_COPILOT":
        if docs: status.append(st["doc_ident"])
        if testing_available and test_details: status.append(st["test_ident"])
        if cert_available and cert_steps: status.append(st["cert_ident"])
        if reqs: status.append(st["req_ident"])

    else:
        status.append(st["official_rec"])

    if not cert_available:
        scheme_name = "N/A"

    NEXT_ACTIONS_TEXT = {
        "en": {
            "consumer_fallback": [
                "Verify the product's BIS licence / applicable identifier.",
                "Check the relevant BIS verification mechanism (like BIS Care app).",
                "Report suspected non-compliance if necessary."
            ],
            "ind_doc": [
                "Check the current BIS application/document checklist.",
                "Prepare the verified documents.",
                "Continue with the applicable BIS application route."
            ],
            "ind_test": [
                "Confirm the applicable standard.",
                "Identify the currently recognised laboratory.",
                "Complete the required testing."
            ],
            "ind_cert": [
                "Confirm certification applicability.",
                "Follow the applicable BIS certification route.",
                "Verify current fees, documents and procedures."
            ],
            "ind_gen": [
                f"Confirm that {record.get('standard_number', 'the standard')} applies to the product.",
                "Review the relevant requirements.",
                "Verify current BIS applicability."
            ]
        },
        "hi": {
            "consumer_fallback": [
                "उत्पाद के BIS लाइसेंस / लागू पहचानकर्ता को सत्यापित करें।",
                "प्रासंगिक BIS सत्यापन तंत्र (जैसे BIS Care ऐप) की जाँच करें।",
                "यदि आवश्यक हो तो संदिग्ध गैर-अनुपालन की रिपोर्ट करें।"
            ],
            "ind_doc": [
                "वर्तमान BIS आवेदन/दस्तावेज़ चेकलिस्ट की जाँच करें।",
                "सत्यापित दस्तावेज़ तैयार करें।",
                "लागू BIS आवेदन मार्ग के साथ जारी रखें।"
            ],
            "ind_test": [
                "लागू मानक की पुष्टि करें।",
                "वर्तमान में मान्यता प्राप्त प्रयोगशाला की पहचान करें।",
                "आवश्यक परीक्षण पूरा करें।"
            ],
            "ind_cert": [
                "प्रमाणन प्रयोज्यता की पुष्टि करें।",
                "लागू BIS प्रमाणन मार्ग का पालन करें।",
                "वर्तमान शुल्क, दस्तावेजों और प्रक्रियाओं को सत्यापित करें।"
            ],
            "ind_gen": [
                f"पुष्टि करें कि {record.get('standard_number', 'मानक')} उत्पाद पर लागू होता है।",
                "प्रासंगिक आवश्यकताओं की समीक्षा करें।",
                "वर्तमान BIS प्रयोज्यता को सत्यापित करें।"
            ]
        },
        "mr": {
            "consumer_fallback": [
                "उत्पादनाचा BIS परवाना / लागू अभिज्ञापकाची पडताळणी करा.",
                "संबंधित BIS पडताळणी यंत्रणा (जसे BIS Care अ‍ॅप) तपासा.",
                "आवश्यक असल्यास संशयित गैर-पालनाची नोंद करा."
            ],
            "ind_doc": [
                "सध्याची BIS अर्ज/दस्तऐवज चेकलिस्ट तपासा.",
                "सत्यापित दस्तऐवज तयार करा.",
                "लागू BIS अर्ज मार्गासह पुढे जा."
            ],
            "ind_test": [
                "लागू मानकाची पुष्टी करा.",
                "सध्या मान्यताप्राप्त प्रयोगशाळेची ओळख पटवा.",
                "आवश्यक चाचणी पूर्ण करा."
            ],
            "ind_cert": [
                "प्रमाणन लागू होण्याच्या शक्यतेची पुष्टी करा.",
                "लागू BIS प्रमाणन मार्गाचा अवलंब करा.",
                "वर्तमान शुल्क, दस्तऐवज आणि प्रक्रियांची पडताळणी करा."
            ],
            "ind_gen": [
                f"पुष्टी करा की {record.get('standard_number', 'मानक')} उत्पादनाला लागू होते.",
                "संबंधित आवश्यकतांचे पुनरावलोकन करा.",
                "सध्याची BIS लागू होण्याची शक्यता पडताळून पहा."
            ]
        }
    }

    na_st = NEXT_ACTIONS_TEXT.get(language, NEXT_ACTIONS_TEXT["en"])

    # Generate dynamic next actions based on mode & intent
    next_actions = []

    if mode == "consumer" or detected_intent in ["CONSUMER_VERIFICATION", "COMPLAINT"]:
        next_actions = i18n_record.get("consumer_actions", record.get("consumer_actions", []))
        if not next_actions:
            next_actions = na_st["consumer_fallback"]
    else:
        # Industry mode actions based on intent
        next_actions = i18n_record.get("industry_actions", record.get("industry_actions", []))
        if not next_actions:
            if detected_intent == "DOCUMENTS":
                next_actions = na_st["ind_doc"]
            elif detected_intent == "TESTING":
                next_actions = na_st["ind_test"]
            elif detected_intent in ["CERTIFICATION", "LICENSING", "SCHEME"]:
                next_actions = na_st["ind_cert"]
            else: # STANDARD or GENERAL
                next_actions = na_st["ind_gen"]

    used_llm = False
    if llm.is_llm_configured():
        system_prompt = (
            f"You are ManakAI, an independent technology prototype. Summarize why this standard applies based ONLY on the following text. "
            f"Do not hallucinate. Respond in {language}. Keep it under 2 sentences."
        )
        user_prompt = f"Product: {title}\nApplicability text: {why_applicable}"
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
        product=title,
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
        disclaimer=DISCLAIMERS.get(language, DISCLAIMERS["en"]),
        answer=composed["answer"],
        why_this_answer=composed["why_this_answer"],
        structured_compliance_journey=record.get("compliance_journey"),
        structured_documents=record.get("documents"),
        structured_testing=record.get("testing") if isinstance(record.get("testing"), dict) else None,
        structured_fees=record.get("fees"),
        regulatory_status=record.get("regulatory_status"),
        official_links=record.get("official_links"),
        structured_evidence=record.get("evidence")
    )
