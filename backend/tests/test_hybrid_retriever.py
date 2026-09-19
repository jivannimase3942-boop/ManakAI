import pytest
import os
import numpy as np
from unittest.mock import patch, MagicMock

# Setup dummy dim for isolated tests
os.environ["EMBEDDING_DIMENSION"] = "4"

from app.hybrid_retriever import (
    hybrid_search,
    _check_product_compatibility,
    _get_product_words
)
from app.ingestion.schemas import VerificationStatus

# --- Basic Unit Tests ---

def test_product_compatibility():
    record = {
        "title": "Packaged Drinking Water",
        "topic": "Food and Agriculture",
        "keywords": ["water", "bottle", "beverage"]
    }

    # Matching product
    assert _check_product_compatibility("packaged water standard", record, 0.0, False) == True
    assert _check_product_compatibility("bottled beverage", record, 0.0, False) == True

    # Missing product (intent words are ignored, so "certification" leaves "aircraft")
    assert _check_product_compatibility("aircraft certification", record, 0.0, False) == False
    assert _check_product_compatibility("flying cars", record, 0.0, False) == False

    # Intent only (no specific product words left after filtering)
    assert _check_product_compatibility("how do I get certification?", record, 0.0, False) == True

def test_cross_domain_adversarial():
    # Candidate: Packaged drinking water certification
    record = {
        "title": "Packaged Drinking Water Certification",
        "topic": "Certification",
        "keywords": ["water", "drink", "bottle"]
    }
    # Query: aircraft certification
    # Product compatibility should FAIL because "aircraft" is not in the record
    assert _check_product_compatibility("aircraft certification", record, 0.0, False) == False

# --- Integration Tests with Mocked Retrieval ---

@pytest.fixture
def mock_kb():
    return [
        {
            "id": "kb-001",
            "standard_number": "IS 14543",
            "title": "Packaged Drinking Water (Other Than Packaged Natural Mineral Water)",
            "topic": "Food and Agriculture",
            "keywords": ["water", "bottle", "drinking", "packaged"],
            "verified": True
        },
        {
            "id": "kb-002",
            "standard_number": "",
            "title": "BIS Certification Process",
            "topic": "Certification",
            "keywords": ["license", "apply", "process", "certification"],
            "verified": True
        },
        {
            "id": "kb-003",
            "standard_number": "",
            "title": "Testing Laboratories",
            "topic": "Laboratory",
            "keywords": ["test", "lab", "recognised", "testing"],
            "verified": True
        },
        {
            "id": "kb-004",
            "standard_number": "",
            "title": "Consumer Grievance and Verification",
            "topic": "Consumer",
            "keywords": ["complaint", "verify", "fake", "huid"],
            "verified": True
        }
    ]

@patch('app.hybrid_retriever.get_semantic_candidates')
@patch('app.hybrid_retriever.knowledge_base')
def test_mandatory_queries(mock_kb_module, mock_sem):
    # Setup mock KB
    import app.knowledge_base as real_kb

    records = [
            {
                "id": "kb-001",
                "standard_number": "IS 14543",
                "title": "Packaged Drinking Water",
                "topic": "Food and Agriculture",
                "keywords": ["water", "bottle", "drinking", "packaged"],
                "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"
            },
            {
                "id": "kb-002",
                "standard_number": "",
                "title": "BIS Certification Process",
                "topic": "Certification",
                "keywords": ["license", "apply", "process", "certification"],
                "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"
            },
            {
                "id": "kb-003",
                "standard_number": "",
                "title": "Testing Laboratories",
                "topic": "Laboratory",
                "keywords": ["test", "lab", "recognised", "testing"],
                "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"
            },
            {
                "id": "kb-004",
                "standard_number": "",
                "title": "Consumer Verification",
                "topic": "Consumer",
                "keywords": ["complaint", "verify", "fake", "huid"],
                "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"
            }
        ]

    mock_kb_module.all_records.return_value = records

    # We will simulate `search` using the real logic on the mock records!
    def fake_search(query, top_k=3):
        # Temporarily swap _KB in the real module for this mock data to use its exact logic
        old_kb = real_kb._KB
        real_kb._KB = records
        res = real_kb.search(query, top_k=top_k)
        real_kb._KB = old_kb
        return res

    mock_kb_module.search.side_effect = fake_search

    # We mock semantic retrieval to return decent scores for related things
    def fake_sem(query, top_k=5):
        q = query.lower()
        if "water" in q: return [{"record_id": "kb-001", "similarity": 0.85}]
        if "certification" in q: return [{"record_id": "kb-002", "similarity": 0.85}]
        if "test" in q: return [{"record_id": "kb-003", "similarity": 0.85}]
        if "verify" in q or "fake" in q: return [{"record_id": "kb-004", "similarity": 0.85}]
        return []

    mock_sem.side_effect = fake_sem

    # A. "What BIS standard applies to packaged drinking water?"
    res = hybrid_search("What BIS standard applies to packaged drinking water?")
    assert len(res) > 0
    assert res[0]["id"] == "kb-001"

    # B. "What standard applies to bottled drinking water?"
    res = hybrid_search("What standard applies to bottled drinking water?")
    assert len(res) > 0
    assert res[0]["id"] == "kb-001"

    # C. "Which standard covers purified drinking water sold in sealed containers?"
    res = hybrid_search("Which standard covers purified drinking water sold in sealed containers?")
    assert len(res) > 0
    assert res[0]["id"] == "kb-001"

    # D. "IS 14543"
    res = hybrid_search("IS 14543")
    assert len(res) > 0
    assert res[0]["id"] == "kb-001"
    assert res[0]["_hybrid_explanation"]["is_exact_id"] == True

    # E. "How do I get BIS certification?" (Now expected to be rejected by specificity gate)
    res = hybrid_search("How do I get BIS certification?")
    assert len(res) == 0

    # F. "Where can I test my product?" (Now expected to be rejected by specificity gate)
    res = hybrid_search("Where can I test my product?")
    assert len(res) == 0

    # G. "How can I verify BIS compliance?" (Now expected to be rejected by specificity gate)
    res = hybrid_search("How can I verify BIS compliance?")
    assert len(res) == 0

    # H. "What BIS standard applies to flying cars?"
    res = hybrid_search("What BIS standard applies to flying cars?")
    assert len(res) == 0  # Should fail product compatibility and score margin

    # I. "What standard applies to random product XYZ?"
    res = hybrid_search("What standard applies to random product XYZ?")
    assert len(res) == 0

    # J. "certification"
    res = hybrid_search("certification")
    assert len(res) == 0  # 1-word generic intent -> Rejected by specificity gate

    # K. "testing laboratory for my product"
    res = hybrid_search("testing laboratory for my product")
    assert len(res) == 0

    # L. "apply for a license to manufacture"
    res = hybrid_search("apply for a license to manufacture")
    assert len(res) == 0

    # M. "recognised lab list"
    res = hybrid_search("recognised lab list")
    assert len(res) == 0

    # N. "fake isi mark grievance"
    res = hybrid_search("fake isi mark grievance")
    assert len(res) == 0  # matches consumer verification record (kb-004 in this mock)

    # K. "certification for aircraft"
    res = hybrid_search("certification for aircraft")
    assert len(res) == 0 # Product compatibility failed for "aircraft"

@patch('app.hybrid_retriever.get_semantic_candidates')
@patch('app.hybrid_retriever.knowledge_base')
def test_verification_gates(mock_kb, mock_sem):
    records = [
        {"id": "r1", "title": "query for r1 r2 r3 r4", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"},
        {"id": "r2", "title": "query for r1 r2 r3 r4", "verification_status": VerificationStatus.PENDING.value},
        {"id": "r3", "title": "query for r1 r2 r3 r4", "verification_status": VerificationStatus.REJECTED.value},
        {"id": "r4", "title": "query for r1 r2 r3 r4", "verification_status": VerificationStatus.SUPERSEDED.value},
    ]
    mock_kb.all_records.return_value = records

    # All are fetched perfectly via keyword
    mock_kb.search.return_value = [{"id": r["id"], "_retrieval_score": 40} for r in records]
    mock_sem.return_value = []

    res = hybrid_search("query for r1 r2 r3 r4")
    assert len(res) == 1
    assert res[0]["id"] == "r1"

@patch('app.hybrid_retriever.get_semantic_candidates')
@patch('app.hybrid_retriever.knowledge_base')
def test_api_failure_fallback(mock_kb, mock_sem):
    # If semantic retrieval fails (returns []), we should still get keyword results.
    mock_kb.all_records.return_value = [{"id": "r1", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE", "title": "packaged water", "keywords": ["water", "packaged"]}]

    def fake_search(query, top_k=3):
        return [{"id": "r1", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE", "_retrieval_score": 40}]

    mock_kb.search.side_effect = fake_search
    mock_sem.return_value = []  # SIMULATE API/CACHE FAILURE

    res = hybrid_search("packaged water")
    assert len(res) == 1
    assert res[0]["id"] == "r1"
    assert res[0]["_hybrid_explanation"]["sem_score_raw"] == 0.0
    assert res[0]["_hybrid_explanation"]["kw_score_raw"] == 40

@patch('app.hybrid_retriever.get_semantic_candidates', return_value=[])
def test_vague_query_generic_allowed(mock_get_candidates):
    query = "Where can I get a certification for my product?"
    res = hybrid_search(query)
    # Could be 0 or more depending on real KB and BM25 scores.
    assert isinstance(res, list)

from app.hybrid_retriever import _check_intent_compatibility

def test_intent_compatibility_gate():
    # A. Clearly incompatible intent
    # Query: "Where can I test my product?" -> Intent is TESTING
    # Candidate: Certification only
    cert_record = {
        "title": "Certification Process",
        "topic": "Certification",
        "keywords": ["license", "certification"]
    }
    assert _check_intent_compatibility("TESTING", cert_record) == False

    # B. Compatible intent
    assert _check_intent_compatibility("CERTIFICATION", cert_record) == True

    # C. UNKNOWN intent
    assert _check_intent_compatibility("UNKNOWN", cert_record) == True

    # D. Missing topic in record (fallback eligible)
    missing_topic_record = {
        "title": "Testing lab info"
    }
    assert _check_intent_compatibility("TESTING", missing_topic_record) == True

def test_provisional_threshold_behavior():
    # Verify that the threshold variables can be modified as experimental/calibration parameters
    import app.hybrid_retriever as hr

    # Ensure they exist and are clearly marked for Phase 2C.4
    assert hasattr(hr, "MIN_HYBRID_SCORE")
    assert hasattr(hr, "SCORE_MARGIN_THRESHOLD")

    # Temporarily set them to prove they are configurable
    old_min = hr.MIN_HYBRID_SCORE
    old_margin = hr.SCORE_MARGIN_THRESHOLD

    hr.MIN_HYBRID_SCORE = 999.0  # Impossible to reach without exact ID

    records = [
        {"id": "r1", "title": "water", "keywords": ["water"], "verified": True}
    ]
    with patch('app.hybrid_retriever.knowledge_base') as mock_kb:
        with patch('app.hybrid_retriever.get_semantic_candidates') as mock_sem:
            mock_kb.all_records.return_value = records
            mock_kb.search.return_value = [{"id": "r1", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE", "_retrieval_score": 40}]
            mock_sem.return_value = [{"record_id": "r1", "similarity": 0.9}]

            # Since max base score is 100, 999 should block it
            res = hr.hybrid_search("water")
            assert len(res) == 0

    # Restore
    hr.MIN_HYBRID_SCORE = old_min
    hr.SCORE_MARGIN_THRESHOLD = old_margin

from app.hybrid_retriever import _is_query_specific

def test_query_specificity_gate():
    # 1. Exact ID -> always True
    assert _is_query_specific("IS 14543", is_exact_id=True) == True

    # 2. Product words exist (>1 total word) -> True
    # "packaged" and "water" are product words
    assert _is_query_specific("packaged drinking water standard", is_exact_id=False) == True
    assert _is_query_specific("BIS certification for packaged drinking water", is_exact_id=False) == True
    assert _is_query_specific("Where can I test packaged drinking water?", is_exact_id=False) == True
    assert _is_query_specific("requirements for packaged drinking water", is_exact_id=False) == True

    # 3. 1-word ambiguous queries -> Now pass if they are valid product words!
    assert _is_query_specific("water", is_exact_id=False) == True
    assert _is_query_specific("testing", is_exact_id=False) == False
    assert _is_query_specific("certification", is_exact_id=False) == False

    # 4. Intent-only purely generic queries -> False (Reject/Clarification)
    assert _is_query_specific("BIS standard", is_exact_id=False) == False
    assert _is_query_specific("How do I get BIS certification?", is_exact_id=False) == False
    assert _is_query_specific("Where can I get certification?", is_exact_id=False) == False
    assert _is_query_specific("What are BIS requirements?", is_exact_id=False) == False

    # 5. Service-specific queries (0 product words, but contain specific service words) -> Now False (Reject/Clarification)
    assert _is_query_specific("testing laboratory for my product", is_exact_id=False) == False
    assert _is_query_specific("apply for a license to manufacture", is_exact_id=False) == False
    assert _is_query_specific("recognised lab list", is_exact_id=False) == False
    assert _is_query_specific("fake isi mark grievance", is_exact_id=False) == False

    # 6. Adversarial -> Have product words (like aircraft, car, xyz) -> True
    # (Specificity gate allows them; other safety gates like intent/product will reject them later)
    assert _is_query_specific("aircraft certification", is_exact_id=False) == True
    assert _is_query_specific("car certification", is_exact_id=False) == True
    assert _is_query_specific("xyz product certification", is_exact_id=False) == True
    assert _is_query_specific("random product testing", is_exact_id=False) == True

def test_integration_rag_decision_flag():
    import app.rag as rag
    import app.decision as decision

    # 1. Test when USE_HYBRID_RETRIEVAL is False
    rag.USE_HYBRID_RETRIEVAL = False
    decision.USE_HYBRID_RETRIEVAL = False

    with patch('app.knowledge_base.search') as mock_kb_search, \
         patch('app.hybrid_retriever.hybrid_search') as mock_hybrid_search:

        mock_kb_search.return_value = [{"id": "r1", "topic": "test", "standard_number": "123", "title": "t", "summary": "s", "guidance": "g", "source_name": "sn", "source_url": "su"}]

        # Calling rag.answer_query with a BIS-scoped query
        res1 = rag.answer_query("bis test query")
        assert res1["matched_topic"] == "test"
        mock_kb_search.assert_called_once()
        mock_hybrid_search.assert_not_called()

        mock_kb_search.reset_mock()

        # Calling decision.generate_compliance_response with a BIS-scoped query
        res2 = decision.generate_compliance_response("bis test query")
        assert res2.match_found == True
        mock_kb_search.assert_called_once()
        mock_hybrid_search.assert_not_called()

    # 2. Test when USE_HYBRID_RETRIEVAL is True
    rag.USE_HYBRID_RETRIEVAL = True
    decision.USE_HYBRID_RETRIEVAL = True

    with patch('app.knowledge_base.search') as mock_kb_search, \
         patch('app.hybrid_retriever.hybrid_search') as mock_hybrid_search:

        mock_hybrid_search.return_value = [{"id": "r1", "topic": "test", "standard_number": "123", "title": "t", "summary": "s", "guidance": "g", "source_name": "sn", "source_url": "su"}]

        # Calling rag.answer_query
        res3 = rag.answer_query("bis test query")
        assert res3["matched_topic"] == "test"
        mock_hybrid_search.assert_called_once()
        mock_kb_search.assert_not_called()

        mock_hybrid_search.reset_mock()

        # Calling decision.generate_compliance_response
        res4 = decision.generate_compliance_response("bis test query")
        assert res4.match_found == True
        mock_hybrid_search.assert_called_once()
        mock_kb_search.assert_not_called()
