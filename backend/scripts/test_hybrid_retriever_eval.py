import os
import json
import numpy as np
from typing import List, Dict, Any
from unittest.mock import patch, MagicMock

# Environment overrides for the test script

os.environ["MIN_HYBRID_SCORE"] = "25.0"
os.environ["SCORE_MARGIN_THRESHOLD"] = "2.0"

from app.hybrid_retriever import hybrid_search, MIN_HYBRID_SCORE, SCORE_MARGIN_THRESHOLD
from app.semantic_retriever import get_semantic_candidates
from app.knowledge_base import search as deterministic_search
from app.ingestion.schemas import VerificationStatus

EVAL_KB = [
    {
        "id": "kb-001",
        "standard_number": "IS 14543",
        "title": "Packaged Drinking Water",
        "topic": "Food and Agriculture",
        "keywords": ["water", "bottle", "drinking", "packaged"],
        "verified": True
    },
    {
        "id": "kb-002",
        "standard_number": "IS 10500",
        "title": "Drinking Water Specification",
        "topic": "Food and Agriculture",
        "keywords": ["drinking", "water", "specification", "tap"],
        "verified": True
    },
    {
        "id": "kb-003",
        "standard_number": "",
        "title": "BIS Certification Process",
        "topic": "Certification",
        "keywords": ["license", "apply", "process", "certification"],
        "verified": True
    },
    {
        "id": "kb-004",
        "standard_number": "",
        "title": "Testing Laboratories",
        "topic": "Laboratory",
        "keywords": ["test", "lab", "recognised", "testing"],
        "verified": True
    },
    {
        "id": "kb-005",
        "standard_number": "",
        "title": "Consumer Verification",
        "topic": "Consumer",
        "keywords": ["complaint", "verify", "fake", "huid"],
        "verified": True
    },
    {
        "id": "kb-006",
        "standard_number": "IS 12345",
        "title": "Aircraft Components",
        "topic": "Engineering",
        "keywords": ["aircraft", "flight", "plane"],
        "verified": True
    },
    {
        "id": "kb-007",
        "standard_number": "IS 99999",
        "title": "Pending Standard",
        "topic": "Engineering",
        "keywords": ["pending", "draft"],
        "verification_status": VerificationStatus.PENDING.value
    },
    {
        "id": "kb-008",
        "standard_number": "IS 88888",
        "title": "Superseded Standard",
        "topic": "Engineering",
        "keywords": ["old", "superseded"],
        "verification_status": VerificationStatus.SUPERSEDED.value
    }
]

QUERIES = [
    # Valid Matches (Specific)
    ("IS 14543", ["kb-001"]),
    ("IS 10500", ["kb-002"]),
    ("packaged drinking water", ["kb-001"]),
    ("bottled water", ["kb-001"]),
    ("drinking water spec", ["kb-002"]),
    ("testing laboratory for my product", ["kb-004"]),
    ("check huid complaint", ["kb-005"]),
    ("IS 12345", ["kb-006"]),
    ("aircraft components", ["kb-006"]),
    ("purified drinking water sold in sealed containers", ["kb-001"]),
    ("tap water standards", ["kb-002"]),
    ("apply for a license to manufacture", ["kb-003"]), # "manufacture" is a product word
    ("recognised lab list", ["kb-004"]), # "list" is a product word
    ("fake isi mark grievance", ["kb-005"]),

    # No Matches (Expected empty / Clarification needed)
    ("How do I get BIS certification?", []), # Intent only -> Reject
    ("bis certification process", []), # Intent only -> Reject
    ("Where can I test my product?", []), # Intent only -> Reject
    ("How can I verify BIS compliance?", []), # Intent only -> Reject
    ("certification", []), # Ambiguous
    ("water", []), # Ambiguous
    ("What BIS standard applies to flying cars?", []), # Unrelated product
    ("certification for aircraft", []), # Cross-domain adversarial
    ("testing for space shuttles", []), # Cross-domain adversarial
    ("How do I verify a UFO?", []), # Cross-domain adversarial
    ("random product xyz", []), # Unknown product
    ("pending draft", []), # PENDING
    ("IS 99999", []), # PENDING Exact ID
    ("old superseded", []), # SUPERSEDED
    ("IS 88888", []), # SUPERSEDED Exact ID
    ("hello there", []), # UNKNOWN intent / Unrelated
]

def mock_semantic_similarity(query: str, top_k: int = 5):
    q = query.lower()
    res = []

    # Simple semantic rules mapping common test phrases to plausible matches

    if "bottled" in q or "sealed" in q or "packaged" in q or "purified" in q:
        res.append({"record_id": "kb-001", "similarity": 0.90})

    if "tap" in q or ("water" in q and "drinking" in q):
        if not any(w in q for w in ["bottled", "sealed", "packaged"]):
            res.append({"record_id": "kb-002", "similarity": 0.88})

    if "water" in q and not res:
        res.append({"record_id": "kb-001", "similarity": 0.80})
        res.append({"record_id": "kb-002", "similarity": 0.80})

    if "certification" in q or "license" in q or "apply" in q:
        res.append({"record_id": "kb-003", "similarity": 0.92})
        # Simulate cross domain
        if "aircraft" in q:
            res.append({"record_id": "kb-003", "similarity": 0.90})

    if "test" in q or "lab" in q:
        res.append({"record_id": "kb-004", "similarity": 0.92})
        if "shuttle" in q:
            res.append({"record_id": "kb-004", "similarity": 0.88})

    if "verify" in q or "compliance" in q or "fake" in q or "complaint" in q:
        res.append({"record_id": "kb-005", "similarity": 0.89})
        if "ufo" in q:
            res.append({"record_id": "kb-005", "similarity": 0.85})

    if "aircraft" in q or "flight" in q:
        res.append({"record_id": "kb-006", "similarity": 0.90})

    if "pending" in q:
        res.append({"record_id": "kb-007", "similarity": 0.95})

    if "superseded" in q or "old" in q:
        res.append({"record_id": "kb-008", "similarity": 0.95})

    if not res:
        # Fallback dummy similarities for random queries
        res.append({"record_id": "kb-001", "similarity": 0.1})

    return sorted(res, key=lambda x: x["similarity"], reverse=True)[:top_k]


def run_evaluation():
    import app.hybrid_retriever as hr
    import app.knowledge_base as real_kb

    # Temporarily mock knowledge base
    original_kb = real_kb._KB
    real_kb._KB = EVAL_KB

    metrics = {
        "valid_match": {"total": 0, "correct": 0, "false_positives": 0, "false_negatives": 0},
        "no_match": {"total": 0, "correct_rejections": 0, "false_positives": 0}
    }

    false_positives_log = []

    with patch('app.hybrid_retriever.get_semantic_candidates', side_effect=mock_semantic_similarity):
        with patch('app.hybrid_retriever.knowledge_base') as mock_kb:
            mock_kb.all_records.return_value = EVAL_KB
            mock_kb.search.side_effect = lambda q, top_k=3: real_kb.search(q, top_k=top_k)

            for query, expected_ids in QUERIES:
                is_valid_query = len(expected_ids) > 0

                hyb = hr.hybrid_search(query, top_k=1)
                hyb_res = [r["id"] for r in hyb]

                if is_valid_query:
                    metrics["valid_match"]["total"] += 1
                    if hyb_res and hyb_res[0] in expected_ids:
                        metrics["valid_match"]["correct"] += 1
                    elif not hyb_res:
                        metrics["valid_match"]["false_negatives"] += 1
                    else:
                        metrics["valid_match"]["false_positives"] += 1
                        false_positives_log.append({
                            "query": query,
                            "expected": expected_ids,
                            "got": hyb_res,
                            "explanation": hyb[0]["_hybrid_explanation"]
                        })
                else:
                    metrics["no_match"]["total"] += 1
                    if not hyb_res:
                        metrics["no_match"]["correct_rejections"] += 1
                    else:
                        metrics["no_match"]["false_positives"] += 1
                        false_positives_log.append({
                            "query": query,
                            "expected": [],
                            "got": hyb_res,
                            "explanation": hyb[0]["_hybrid_explanation"]
                        })

    real_kb._KB = original_kb

    print(f"Hybrid Retriever Robustness Evaluation (30 cases)")
    print(f"=================================================")
    print(f"Thresholds: MIN_SCORE={hr.MIN_HYBRID_SCORE}, MARGIN={hr.SCORE_MARGIN_THRESHOLD}")
    print(f"")
    print(f"[Valid-Match Queries] Total: {metrics['valid_match']['total']}")
    print(f"  Correct Matches: {metrics['valid_match']['correct']}")
    print(f"  False Positives: {metrics['valid_match']['false_positives']}")
    print(f"  False Negatives: {metrics['valid_match']['false_negatives']}")
    print(f"")
    print(f"[No-Match Queries] Total: {metrics['no_match']['total']}")
    print(f"  Correct Rejections: {metrics['no_match']['correct_rejections']}")
    print(f"  False Positives: {metrics['no_match']['false_positives']}")
    print(f"")

    if false_positives_log:
        print(f"False Positive Details:")
        for fp in false_positives_log:
            print(f"  - Query: '{fp['query']}'")
            print(f"    Expected: {fp['expected']}, Got: {fp['got']}")
            print(f"    Scores: Base KW: {fp['explanation']['kw_score_raw']}, Sem: {fp['explanation']['sem_score_raw']}, Final: {fp['explanation']['final_score']}")
            print(f"    Why it passed: The semantic score combined with some kw overlap or fallback allowed it to pass the minimum score threshold of 25.0, and the intent/product gates were not triggered to block it.")
    else:
        print("No false positives observed!")

if __name__ == "__main__":
    run_evaluation()
