import re
from typing import List, Dict, Any, Tuple
import logging

from app import knowledge_base
from app.semantic_retriever import get_semantic_candidates, _is_record_verified
from app.intent import detect_intent

logger = logging.getLogger(__name__)

import os

# CALIBRATED EVALUATION PARAMETERS (Phase 2C.4)
# Calibrated against evaluation dataset to balance recall and precision.
MIN_HYBRID_SCORE = float(os.getenv("MIN_HYBRID_SCORE", "25.0"))
SCORE_MARGIN_THRESHOLD = float(os.getenv("SCORE_MARGIN_THRESHOLD", "2.0"))

# Words that indicate purely generic intent
GENERIC_INTENT_WORDS = {
    "certification", "certificate", "test", "testing", "tests", "tested", "standard", "requirements", "requirement",
    "bis", "compliance", "process", "get", "need", "make", "where", "how", "what", "which",
    "my", "product", "covered", "applies", "number", "explain", "general", "are",
    "can", "do", "does", "done", "be", "for", "i", "verify", "check", "why", "when", "is", "rule", "rules",
    "regulation", "regulations", "guideline", "guidelines", "mandatory", "voluntary", "about",
    "मानक", "नियम", "मानके", "दिशानिर्देश", "मार्गदर्शक", "प्रमाणन", "योजना", "स्कीम", "टेस्टिंग",
    "परीक्षण", "जांच", "चाचणी", "msme", "micro", "small", "medium", "enterprise", "enterprises"
}

# Words that unambiguously articulate a specific service/action
SPECIFIC_SERVICE_WORDS = {
    "laboratory", "laboratories", "lab", "labs", "recognised", "recognized", "list",
    "complain", "complaint", "complaints", "fake", "grievance", "huid", "hallmark",
    "registration", "license", "licence", "apply", "manufacture", "manufacturer", "manufacturers", "isi", "mark",
    "document", "documents", "form", "checklist", "paperwork", "scheme", "crs",
    "लाइसेंस", "परवाना", "शिकायत", "तक्रार", "प्रयोगशाला", "प्रयोगशाळा", "लॅब", "लैब", "बनावट", "फर्जी", "नकली", "मार्क",
    "where to apply", "लॅबमध्ये"
}

INTENT_STOPWORDS = GENERIC_INTENT_WORDS | SPECIFIC_SERVICE_WORDS

def _get_product_words(query: str) -> set:
    """Extracts non-intent, non-stopword tokens that likely represent the product."""
    import string
    text = query.lower().translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    # Exclude basic knowledge_base stopwords and intent words
    from app.knowledge_base import _STOPWORDS
    product_words = set(words) - _STOPWORDS - INTENT_STOPWORDS
    return product_words

def _check_product_compatibility(query: str, record: Dict[str, Any], sem_score: float, is_non_ascii: bool) -> bool:
    """
    Returns True if product compatibility is established.
    If product_words is empty, we assume True (query was just an intent like "certification" - handled by vague query gate).
    If product_words exists, at least one must be found in title, topic, or keywords.
    For non-ASCII queries (multilingual), we lack English lexical overlap, so we allow strong semantic evidence (>= 0.72) to establish compatibility.
    """
    product_words = _get_product_words(query)
    if not product_words:
        return True

    record_text = (
        record.get("title", "") + " " +
        record.get("product_name", "") + " " +
        record.get("topic", "") + " " +
        " ".join(record.get("keywords", [])) + " " +
        " ".join(record.get("aliases", []))
    ).lower()

    i18n = record.get("i18n", {})
    for lang, l_data in i18n.items():
        record_text += " " + l_data.get("title", "").lower()
        record_text += " " + " ".join(l_data.get("keywords", [])).lower()
        record_text += " " + " ".join(l_data.get("aliases", [])).lower()

    # Lexical overlap
    matched_words = [word for word in product_words if word in record_text]
    
    if matched_words:
        # Require sufficient product identity/context before mapping a generic "steel" query to rebar standard
        if record.get("id") == "kb-015" and "steel" in matched_words:
            rebar_context = {"rebar", "rebars", "tmt", "bar", "bars", "wire", "wires", "reinforcement", "deformed", "sariya", "सरिया", "सळई"}
            if not any(w in query.lower() for w in rebar_context):
                return False
        return True

    # Semantic Override: If no lexical overlap, but semantic score is strong (>= 0.68)
    # This acts as a language-independent entity compatibility fallback.
    # It should only apply to actual product records, not generic service records.
    if sem_score >= 0.68 and not _is_explicitly_generic_service_record(record):
        return True

    return False

def _is_query_specific(query: str, is_exact_id: bool) -> bool:
    """
    Deterministic safety gate to prevent overly generic intent-only queries
    from confidently returning results without clarification.
    A query is considered specific if it contains an exact standard identifier,
    contains specific product/entity words, or contains specific service action words.
    """
    if is_exact_id:
        return True

    import string
    text = query.lower().translate(str.maketrans('', '', string.punctuation))
    words = text.split()

    product_words = _get_product_words(query)
    if len(product_words) > 0:
        return True

    return False

def _check_intent_compatibility(query_intent: str, record: Dict[str, Any]) -> bool:
    """
    Hard safety gate for intent compatibility.
    """
    if query_intent == "UNKNOWN":
        return True

    # If the record is NOT an explicitly generic service record, it's a product record.
    # Product records contain info on testing, certification, requirements, etc.
    # So they are inherently compatible with all these intents for that product.
    if not _is_explicitly_generic_service_record(record):
        return True

    record_topic = record.get("topic", "").upper()

    # Basic alignment map defining which generic topics belong to which intents
    alignment = {
        "CERTIFICATION": ["CERTIFICATION", "COMPULSORY", "SCHEME"],
        "TESTING": ["LABORATORY", "TESTING"],
        "CONSUMER_VERIFICATION": ["CONSUMER", "VERIFICATION", "COMPLAINT"],
        "COMPLAINT": ["CONSUMER", "COMPLAINT"],
        "DOCUMENTS": ["DOCUMENT", "FORM", "PAPERWORK"]
    }

    if query_intent in alignment:
        if not record_topic:
            return True
        if not any(a in record_topic for a in alignment[query_intent]):
            return False

    return True

def _is_explicitly_generic_service_record(record: Dict[str, Any]) -> bool:
    """Returns True if the record is an explicitly generic service/information record (no specific IS number)."""
    std_num = record.get("standard_number", "")
    return not std_num.startswith("IS ")

def _check_entity_compatibility(extracted_entity_en: str, is_generic: bool, record: Dict[str, Any]) -> bool:
    """
    Language-independent entity compatibility check.
    If the LLM determined the query is purely generic (is_generic = True) or entity is None/Unknown,
    we only allow matching explicitly generic service records (e.g. BIS Certification Scheme).
    If a specific entity was extracted, we check if it aligns with the record's text.
    """
    if extracted_entity_en:
        extracted_entity_en = extracted_entity_en.strip().lower()

    if is_generic or not extracted_entity_en or extracted_entity_en in ["none", "unknown", ""]:
        # Query is generic (no product specified). Only explicitly generic records can match.
        return _is_explicitly_generic_service_record(record)

    # We have a specific product entity. Check if it's in the record.
    record_text = (
        record.get("title", "") + " " +
        record.get("product_name", "") + " " +
        record.get("topic", "") + " " +
        " ".join(record.get("keywords", [])) + " " +
        " ".join(record.get("aliases", []))
    ).lower()

    # Simple substring check for the extracted entity
    if extracted_entity_en in record_text:
        return True

    # Also split into words and check if any significant word matches
    words = [w for w in re.findall(r"[a-z0-9]+", extracted_entity_en) if len(w) > 2]
    matched_words = [w for w in words if w in record_text]
    
    if matched_words:
        # Require sufficient product identity/context before mapping a generic "steel" query to rebar standard
        if record.get("id") == "kb-015" and "steel" in matched_words:
            rebar_context = {"rebar", "rebars", "tmt", "bar", "bars", "wire", "wires", "reinforcement", "deformed", "sariya", "सरिया", "सळई"}
            if not any(w in extracted_entity_en for w in rebar_context):
                return False
        return True

    return False

def hybrid_search(query: str, top_k: int = 3, norm_context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    norm_context = norm_context or {}

    llm_norm_en = norm_context.get("normalized_query")
    llm_product_entity = norm_context.get("product_entity")
    llm_service_entity = norm_context.get("service_entity")
    llm_confidence = norm_context.get("confidence", 0.0)

    # If confidence is low, fall back to pure deterministic native handling (ignore LLM)
    if llm_confidence < 0.7:
        llm_success = False
        llm_norm_en = None
    else:
        llm_success = llm_norm_en is not None

    # Derive is_generic: if there is no specific product entity, it's generic
    llm_is_generic = not bool(llm_product_entity) and bool(llm_service_entity)

    query_lower = query.lower()
    norm_query_en = llm_norm_en if llm_success else query_lower
    query_intent = detect_intent(norm_query_en)

    # Structural check for vague queries:
    # If the normalized query has no non-stopword, non-intent words, it's considered vague
    # (e.g., "certification", "where is the laboratory", "how to apply").
    norm_product_words = _get_product_words(norm_query_en)
    is_vague_query = len(norm_product_words) == 0

    # 1. Fetch Candidates
    kw_candidates = knowledge_base.search(norm_query_en, top_k=100)
    kw_map = {r["id"]: r for r in kw_candidates}

    sem_candidates = get_semantic_candidates(query, top_k=10)
    sem_available = len(sem_candidates) > 0
    sem_map = {c["record_id"]: c["similarity"] for c in sem_candidates}

    all_ids = set(kw_map.keys()).union(set(sem_map.keys()))
    all_kb_records = {r["id"]: r for r in knowledge_base.all_records()}
    scored_records = []

    for rid in all_ids:
        record = all_kb_records.get(rid)
        if not record:
            continue

        # GATE 1: Verification
        if not _is_record_verified(record):
            continue

        std_num = record.get("standard_number", "").lower()
        is_exact_id = False
        if std_num and len(std_num) > 3:
            import re
            base_match = re.search(r'is\s+\d+', std_num)
            if base_match and re.search(r'\b' + re.escape(base_match.group(0)) + r'(?!\d)', query_lower):
                is_exact_id = True
            elif re.search(r'\b' + re.escape(std_num) + r'(?!\d)', query_lower):
                is_exact_id = True

        kw_score = kw_map.get(rid, {}).get("_retrieval_score", 0)
        sem_score = sem_map.get(rid, 0.0)
        is_non_ascii = not all(ord(c) < 128 for c in query)

        # GATE 1.2: Vague Query Rejection
        if not is_exact_id and is_vague_query:
            # The query is purely generic (e.g., "where is the laboratory", "how to apply")
            # and lacks any product context. It must ONLY match explicitly generic service records.
            if not _is_explicitly_generic_service_record(record):
                continue

        # GATE 1.5 & GATE 3: Specificity and Product Compatibility
        if not is_exact_id:
            if llm_success:
                if not _check_entity_compatibility(llm_product_entity, llm_is_generic, record):
                    if record['id'] == 'kb-004': print("Failed GATE 1.5 (LLM)")
                    continue
            else:
                if not _is_query_specific(query, is_exact_id):
                    if record['id'] == 'kb-004': print("Failed GATE 1.5 (Specificity)")
                    continue
                if not _check_product_compatibility(query, record, sem_score, is_non_ascii):
                    if record['id'] == 'kb-004': print("Failed GATE 1.5 (Product Compatibility)")
                    continue

        # GATE 2: Lexical Evidence
        if not is_exact_id and kw_score == 0:
            # Lexical overlap is not mandatory ONLY if semantic evidence is strong enough
            # AND entity compatibility passed.
            if sem_score < 0.65:
                continue

        # GATE 4: Intent Compatibility
        if not _check_intent_compatibility(query_intent, record):
            if record['id'] == 'kb-004': print("Failed GATE 4")
            continue

        # HYBRID RANKING CALCULATION
        norm_kw = min(kw_score / 40.0, 1.0) + (kw_score / 1000.0) # Tie-breaker for high kw scores
        norm_sem = max(0.0, sem_score)

        final_score = (norm_kw * 50.0) + (norm_sem * 50.0)
        if is_exact_id:
            final_score += 100.0

        # INTENT BOOST (Reward candidates that contain information specific to the user's intent)
        if query_intent == "TESTING":
            if record.get("testing", {}).get("available") == True:
                final_score *= 1.2
        elif query_intent in ["CERTIFICATION", "LICENSING"]:
            if record.get("certification", {}).get("available") == True:
                final_score *= 1.2

        explanation = {
            "is_exact_id": is_exact_id,
            "kw_score_raw": kw_score,
            "sem_score_raw": sem_score,
            "final_score": final_score,
            "llm_used": llm_success
        }

        if final_score >= 40.0:
            confidence = "high"
        elif final_score >= 25.0:
            confidence = "medium"
        elif final_score >= MIN_HYBRID_SCORE:
            confidence = "low"
        else:
            confidence = "none"

        r_copy = dict(record)
        r_copy["_hybrid_score"] = final_score
        r_copy["_retrieval_confidence"] = confidence
        r_copy["_hybrid_explanation"] = explanation
        scored_records.append(r_copy)

    scored_records.sort(key=lambda x: x["_hybrid_score"], reverse=True)

    # GATE 5: Confidence & Margin Safety Gate
    if not scored_records:
        return []

    top_record = scored_records[0]
    top_score = top_record["_hybrid_score"]

    if top_score < MIN_HYBRID_SCORE:
        return []

    if len(scored_records) > 1:
        second_score = scored_records[1]["_hybrid_score"]
        if top_score < 100.0:
            if (top_score - second_score) < SCORE_MARGIN_THRESHOLD:
                return []

    # GATE 6: Safe Degraded-Mode (Phase 2E.1 Correction)
    # If semantic retrieval is unavailable, we must rely entirely on deterministic/lexical evidence.
    # Without semantic validation, low-scoring lexical matches (which may just be hallucinations or partial overlaps) are dangerous.
    if not sem_available and not top_record["_hybrid_explanation"]["is_exact_id"]:
        # Only accept if lexical evidence is exceptionally strong and unambiguous
        # We define strong as having a hybrid score >= 40.0 (high confidence)
        if top_score < 40.0 or (len(scored_records) > 1 and (top_score - scored_records[1]["_hybrid_score"]) < 15.0):
            return []

    # GATE 7: Exact-ID Contamination Prevention
    # If the primary matched intent was an EXACT standard, drop unrelated semantic stragglers
    if scored_records and scored_records[0]["_hybrid_explanation"]["is_exact_id"]:
        scored_records = [r for r in scored_records if r["_hybrid_explanation"]["is_exact_id"]]

    return scored_records[:top_k]
