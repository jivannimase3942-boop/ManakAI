import logging
import numpy as np
from typing import List, Dict, Any, Optional

from app.embeddings import get_embedding, EmbeddingCacheManager
from app import knowledge_base
from app.ingestion.schemas import VerificationStatus

logger = logging.getLogger(__name__)

def safe_cosine_similarity(query_vec: np.ndarray, doc_vectors: np.ndarray) -> np.ndarray:
    """
    Computes cosine similarity between a 1D query vector and a 2D matrix of doc vectors safely.
    Handles zero vectors by assigning 0.0 similarity.
    """
    if query_vec.ndim != 1:
        query_vec = query_vec.flatten()

    if doc_vectors.ndim == 1:
        doc_vectors = doc_vectors.reshape(1, -1)

    if query_vec.shape[0] != doc_vectors.shape[1]:
        logger.error(f"Dimension mismatch: query {query_vec.shape}, docs {doc_vectors.shape}")
        return np.zeros(doc_vectors.shape[0])

    query_norm = np.linalg.norm(query_vec)
    if query_norm == 0:
        return np.zeros(doc_vectors.shape[0])

    doc_norms = np.linalg.norm(doc_vectors, axis=1)

    # Avoid division by zero
    valid_docs = doc_norms > 0
    similarities = np.zeros(doc_vectors.shape[0])

    similarities[valid_docs] = np.dot(doc_vectors[valid_docs], query_vec) / (doc_norms[valid_docs] * query_norm)

    # Ensure numerical stability bounds
    similarities = np.clip(similarities, -1.0, 1.0)

    return similarities

def _is_record_verified(record: Optional[Dict[str, Any]]) -> bool:
    """
    Live retrieval must require ALL of:
    status == 'VERIFIED' AND verified == true AND verification_status == 'OFFICIAL_EVIDENCE'
    """
    if not record:
        return False

    if record.get("status") != "VERIFIED":
        return False

    if record.get("verified") is not True:
        return False

    if record.get("verification_status") != "OFFICIAL_EVIDENCE":
        return False

    return True

def get_semantic_candidates(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Isolated semantic retriever component.
    Returns ranked candidate records based solely on semantic similarity.
    Does NOT assert that the standard applies.
    """
    manager = EmbeddingCacheManager()
    embeddings, cached_record_ids = manager.load_cache()

    if embeddings is None or cached_record_ids is None or len(cached_record_ids) == 0:
        logger.warning("Semantic retrieval aborted: Invalid or missing embedding cache.")
        return []

    # Validate embeddings format
    if not isinstance(embeddings, np.ndarray) or embeddings.ndim != 2:
        logger.error(f"Semantic retrieval aborted: Embeddings cache is not a 2D numpy array.")
        return []

    # Validate dimension matches config
    from app.embeddings import EMBEDDING_DIMENSION
    if embeddings.shape[1] != EMBEDDING_DIMENSION:
        logger.error(f"Semantic retrieval aborted: Cache embedding dimension {embeddings.shape[1]} != config {EMBEDDING_DIMENSION}.")
        return []

    # Validate row count matches ID count
    if embeddings.shape[0] != len(cached_record_ids):
        logger.error(f"Semantic retrieval aborted: Row count {embeddings.shape[0]} != ID count {len(cached_record_ids)}.")
        return []

    # Validate record IDs are non-empty
    if any(not str(rid).strip() for rid in cached_record_ids):
        logger.error("Semantic retrieval aborted: Cache contains empty or invalid record IDs.")
        return []

    query_vec = get_embedding(query)
    if query_vec is None:
        logger.warning("Semantic retrieval aborted: Query embedding generation failed.")
        return []

    similarities = safe_cosine_similarity(query_vec, embeddings)

    # Map back to records and verify status
    all_kb_records = {r["id"]: r for r in knowledge_base.all_records()}

    candidates = []
    for idx, record_id in enumerate(cached_record_ids):
        # We assume the record might be in the legacy KB JSON
        # (Later phases will query the unified DB)
        record = all_kb_records.get(record_id)

        if _is_record_verified(record):
            candidates.append({
                "record_id": record_id,
                "similarity": float(similarities[idx])
            })

    # Sort descending
    candidates.sort(key=lambda x: x["similarity"], reverse=True)

    return candidates[:top_k]
