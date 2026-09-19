import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from app.semantic_retriever import safe_cosine_similarity, get_semantic_candidates, _is_record_verified
from app.ingestion.schemas import VerificationStatus
import os
os.environ["EMBEDDING_DIMENSION"] = "2"  # Set to 2 for easier testing of 2D vectors

def test_safe_cosine_similarity_correctness():
    # Identical vectors should have similarity 1.0
    q = np.array([1.0, 0.0])
    docs = np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]])
    sims = safe_cosine_similarity(q, docs)
    assert np.isclose(sims[0], 1.0)
    assert np.isclose(sims[1], 0.0)
    assert np.isclose(sims[2], -1.0)

def test_safe_cosine_similarity_zero_vectors():
    q = np.array([0.0, 0.0])
    docs = np.array([[1.0, 0.0], [0.0, 0.0]])
    sims = safe_cosine_similarity(q, docs)
    assert sims[0] == 0.0
    assert sims[1] == 0.0

def test_safe_cosine_similarity_dimension_mismatch():
    q = np.array([1.0, 0.0, 1.0])
    docs = np.array([[1.0, 0.0]])
    sims = safe_cosine_similarity(q, docs)
    # Should safely return zeros of correct doc length
    assert len(sims) == 1
    assert sims[0] == 0.0

def test_record_verified_adapter():
    assert _is_record_verified(None) == False
    assert _is_record_verified({"id": "kb-001", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"}) == True
    assert _is_record_verified({"id": "kb-001", "status": "VERIFIED", "verified": False, "verification_status": "OFFICIAL_EVIDENCE"}) == False
    assert _is_record_verified({"id": "ing-001", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"}) == True
    assert _is_record_verified({"id": "ing-001", "status": "PENDING", "verified": False, "verification_status": VerificationStatus.PENDING.value}) == False
    assert _is_record_verified({"id": "ing-001", "status": "REJECTED", "verified": False, "verification_status": VerificationStatus.REJECTED.value}) == False
    assert _is_record_verified({"id": "ing-001", "status": "SUPERSEDED", "verified": False, "verification_status": VerificationStatus.SUPERSEDED.value}) == False

@patch('app.semantic_retriever.EmbeddingCacheManager')
@patch('app.semantic_retriever.get_embedding')
@patch('app.semantic_retriever.knowledge_base')
def test_missing_cache_graceful_fail(mock_kb, mock_embed, mock_cache_cls):
    mock_manager = MagicMock()
    mock_manager.load_cache.return_value = (None, None)
    mock_cache_cls.return_value = mock_manager

    results = get_semantic_candidates("test")
    assert results == []

@patch('app.semantic_retriever.EmbeddingCacheManager')
@patch('app.semantic_retriever.get_embedding')
@patch('app.semantic_retriever.knowledge_base')
def test_embedding_api_failure_graceful_fail(mock_kb, mock_embed, mock_cache_cls):
    mock_manager = MagicMock()
    # Need to match default 768 dimensions config to pass format validation, or mock it
    mock_manager.load_cache.return_value = (np.zeros((1, 768)), ["r1"])
    mock_cache_cls.return_value = mock_manager

    mock_embed.return_value = None

    with patch('app.embeddings.EMBEDDING_DIMENSION', 768):
        results = get_semantic_candidates("test")
    assert results == []

@patch('app.semantic_retriever.EmbeddingCacheManager')
@patch('app.semantic_retriever.get_embedding')
@patch('app.semantic_retriever.knowledge_base')
def test_cache_row_count_mismatch_graceful_fail(mock_kb, mock_embed, mock_cache_cls):
    mock_manager = MagicMock()
    # 2 rows, but only 1 record ID
    mock_manager.load_cache.return_value = (np.zeros((2, 768)), ["r1"])
    mock_cache_cls.return_value = mock_manager

    with patch('app.embeddings.EMBEDDING_DIMENSION', 768):
        results = get_semantic_candidates("test")
    assert results == []

@patch('app.semantic_retriever.EmbeddingCacheManager')
@patch('app.semantic_retriever.get_embedding')
@patch('app.semantic_retriever.knowledge_base')
def test_cache_dimension_mismatch_graceful_fail(mock_kb, mock_embed, mock_cache_cls):
    mock_manager = MagicMock()
    # Dimension is 100, but config default is 768
    mock_manager.load_cache.return_value = (np.zeros((1, 100)), ["r1"])
    mock_cache_cls.return_value = mock_manager

    with patch('app.embeddings.EMBEDDING_DIMENSION', 768):
        results = get_semantic_candidates("test")
    assert results == []

@patch('app.semantic_retriever.EmbeddingCacheManager')
@patch('app.semantic_retriever.get_embedding')
@patch('app.semantic_retriever.knowledge_base')
def test_cache_not_2d_array_graceful_fail(mock_kb, mock_embed, mock_cache_cls):
    mock_manager = MagicMock()
    mock_manager.load_cache.return_value = (np.zeros(768), ["r1"]) # 1D array
    mock_cache_cls.return_value = mock_manager

    with patch('app.embeddings.EMBEDDING_DIMENSION', 768):
        results = get_semantic_candidates("test")
    assert results == []

@patch('app.semantic_retriever.EmbeddingCacheManager')
@patch('app.semantic_retriever.get_embedding')
@patch('app.semantic_retriever.knowledge_base')
def test_semantic_ranking_and_mapping(mock_kb, mock_embed, mock_cache_cls):
    mock_manager = MagicMock()
    # Cache has 3 records
    mock_manager.load_cache.return_value = (
        np.array([[1.0, 0.0], [0.0, 1.0], [0.707, 0.707]]),
        ["r1", "r2", "r3"]
    )
    mock_cache_cls.return_value = mock_manager

    # Query aligns perfectly with r1
    mock_embed.return_value = np.array([1.0, 0.0])

    mock_kb.all_records.return_value = [
        {"id": "r1", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"},
        {"id": "r2", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"},
        {"id": "r3", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"}
    ]

    with patch('app.embeddings.EMBEDDING_DIMENSION', 2):
        results = get_semantic_candidates("query")
    assert len(results) == 3
    assert results[0]["record_id"] == "r1"
    assert np.isclose(results[0]["similarity"], 1.0)
    assert results[1]["record_id"] == "r3"
    assert np.isclose(results[1]["similarity"], 0.707, atol=1e-3)
    assert results[2]["record_id"] == "r2"
    assert np.isclose(results[2]["similarity"], 0.0)

@patch('app.semantic_retriever.EmbeddingCacheManager')
@patch('app.semantic_retriever.get_embedding')
@patch('app.semantic_retriever.knowledge_base')
def test_exclusion_of_unverified_records(mock_kb, mock_embed, mock_cache_cls):
    mock_manager = MagicMock()
    mock_manager.load_cache.return_value = (
        np.array([[1.0, 0.0], [1.0, 0.0], [1.0, 0.0], [1.0, 0.0]]),
        ["r_verified", "r_pending", "r_rejected", "r_superseded"]
    )
    mock_cache_cls.return_value = mock_manager
    mock_embed.return_value = np.array([1.0, 0.0])

    mock_kb.all_records.return_value = [
        {"id": "r_verified", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"},
        {"id": "r_pending", "status": "PENDING", "verified": False, "verification_status": VerificationStatus.PENDING.value},
        {"id": "r_rejected", "status": "REJECTED", "verified": False, "verification_status": VerificationStatus.REJECTED.value},
        {"id": "r_superseded", "status": "SUPERSEDED", "verified": False, "verification_status": VerificationStatus.SUPERSEDED.value}
    ]

    with patch('app.embeddings.EMBEDDING_DIMENSION', 2):
        results = get_semantic_candidates("query")
    # Only the verified record should be returned
    assert len(results) == 1
    assert results[0]["record_id"] == "r_verified"

# --- Evaluation Fixture Mocking Existing KB ---

@patch('app.semantic_retriever.EmbeddingCacheManager')
@patch('app.semantic_retriever.get_embedding')
@patch('app.semantic_retriever.knowledge_base')
def test_evaluation_fixture(mock_kb, mock_embed, mock_cache_cls):
    # Mocking the actual 8 KB records
    mock_manager = MagicMock()
    # Let's say vector mapping:
    # 0: kb-001 Packaged water
    # 1: kb-002 Certification
    # 2: kb-004 Testing Lab
    # 3: kb-006 Consumer grievance
    mock_manager.load_cache.return_value = (
        np.array([
            [1.0, 0.0, 0.0, 0.0], # kb-001
            [0.0, 1.0, 0.0, 0.0], # kb-002
            [0.0, 0.0, 1.0, 0.0], # kb-004
            [0.0, 0.0, 0.0, 1.0], # kb-006
        ]),
        ["kb-001", "kb-002", "kb-004", "kb-006"]
    )
    mock_cache_cls.return_value = mock_manager

    mock_kb.all_records.return_value = [
        {"id": "kb-001", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"},
        {"id": "kb-002", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"},
        {"id": "kb-004", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"},
        {"id": "kb-006", "status": "VERIFIED", "verified": True, "verification_status": "OFFICIAL_EVIDENCE"},
    ]

    # Paraphrase match: "purified H2O for drinking" matches kb-001 highly
    mock_embed.return_value = np.array([0.9, 0.1, 0.0, 0.0])
    with patch('app.embeddings.EMBEDDING_DIMENSION', 4):
        res = get_semantic_candidates("purified H2O for drinking")
    assert res[0]["record_id"] == "kb-001"

    # Certification query
    mock_embed.return_value = np.array([0.0, 0.95, 0.0, 0.0])
    with patch('app.embeddings.EMBEDDING_DIMENSION', 4):
        res = get_semantic_candidates("How do I get BIS certification")
    assert res[0]["record_id"] == "kb-002"

    # Testing query
    mock_embed.return_value = np.array([0.0, 0.0, 0.95, 0.0])
    with patch('app.embeddings.EMBEDDING_DIMENSION', 4):
        res = get_semantic_candidates("Where can I test my product")
    assert res[0]["record_id"] == "kb-004"

    # Consumer query
    mock_embed.return_value = np.array([0.0, 0.0, 0.0, 0.95])
    with patch('app.embeddings.EMBEDDING_DIMENSION', 4):
        res = get_semantic_candidates("Verify my BIS complaint")
    assert res[0]["record_id"] == "kb-006"

    # Unrelated negative query (flying cars) should yield low scores
    mock_embed.return_value = np.array([-0.1, -0.1, 0.0, 0.0])
    with patch('app.embeddings.EMBEDDING_DIMENSION', 4):
        res = get_semantic_candidates("flying cars certification")
    # In Phase 2C.2, the semantic retriever just returns the sorted list regardless of how low it is.
    # The top score will be 0.0 (or very low), the safety threshold will drop it in Phase 2C.3.
    assert len(res) == 4
    assert res[0]["similarity"] <= 0.0
