import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.ERROR)

# Load env variables (including GEMINI_API_KEY)
load_dotenv(".env")

# Must set before importing app modules

os.environ["MIN_HYBRID_SCORE"] = "25.0"
os.environ["SCORE_MARGIN_THRESHOLD"] = "2.0"

import json
from typing import List, Dict, Any
from unittest.mock import patch

from app.hybrid_retriever import hybrid_search, MIN_HYBRID_SCORE, SCORE_MARGIN_THRESHOLD
from app.semantic_retriever import get_semantic_candidates
from app.knowledge_base import search as deterministic_search
from app.ingestion.schemas import VerificationStatus
from app.embeddings import EmbeddingCacheManager, get_embedding

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
    ("apply for a license to manufacture", ["kb-003"]),
    ("recognised lab list", ["kb-004"]),
    ("fake isi mark grievance", ["kb-005"]),

    # No Matches (Expected empty / Clarification needed)
    ("How do I get BIS certification?", []),
    ("bis certification process", []),
    ("Where can I test my product?", []),
    ("How can I verify BIS compliance?", []),
    ("certification", []),
    ("water", []),
    ("What BIS standard applies to flying cars?", []),
    ("certification for aircraft", []),
    ("testing for space shuttles", []),
    ("How do I verify a UFO?", []),
    ("random product xyz", []),
    ("pending draft", []),
    ("IS 99999", []),
    ("old superseded", []),
    ("IS 88888", []),
    ("hello there", []),
]

def run_evaluation():
    import app.hybrid_retriever as hr
    import app.knowledge_base as real_kb
    import app.embeddings as real_emb

    # Create temp files for real cache generation
    EVAL_KB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "eval_knowledge_base.json")
    EVAL_CACHE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "eval_embeddings_cache.npz")

    with open(EVAL_KB_PATH, "w") as f:
        json.dump(EVAL_KB, f)

    print("Testing real embedding generation and cache...")

    with patch('app.embeddings.KB_PATH', EVAL_KB_PATH), \
         patch('app.embeddings.CACHE_PATH', EVAL_CACHE_PATH), \
         patch('app.embeddings._compute_kb_hash', lambda: "dummy_hash"), \
         patch('app.semantic_retriever.EmbeddingCacheManager', lambda: EmbeddingCacheManager(cache_path=EVAL_CACHE_PATH)):

        # Test batch query directly to find why it fails
        try:
            b_res = real_emb._CLIENT.models.embed_content(
                model=real_emb.GEMINI_EMBEDDING_MODEL,
                contents=["test1", "test2"],
                config=real_emb.types.EmbedContentConfig(
                    output_dimensionality=real_emb.EMBEDDING_DIMENSION
                )
            )
            print("Batch test raw result length:", len(b_res.embeddings) if b_res.embeddings else "None")
        except Exception as e:
            print("Batch test error:", e)

        # Test basic query embedding
        test_vec = get_embedding("test query")
        if test_vec is None:
            print("FAILED: get_embedding returned None. Check API key or connection.")
            return

        print(f"Generated query embedding shape: {test_vec.shape}")

        # Build cache
        manager = EmbeddingCacheManager(cache_path=EVAL_CACHE_PATH)
        success = manager.build_and_save_cache(EVAL_KB)
        if not success:
            print("FAILED: Cache generation failed.")
            return

        print("Successfully generated and saved real .npz cache.")

        # Reload cache test
        emb, rids = manager.load_cache()
        if emb is None:
            print("FAILED: Could not reload cache.")
            return

        print(f"Cache reloaded successfully. Shape: {emb.shape}")

        # Now run hybrid search
        original_kb = real_kb._KB
        real_kb._KB = EVAL_KB

        metrics = {
            "valid_match": {"total": 0, "correct": 0, "false_positives": 0, "false_negatives": 0},
            "no_match": {"total": 0, "correct_rejections": 0, "false_positives": 0}
        }

        false_positives_log = []
        false_negatives_log = []

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
                        false_negatives_log.append({"query": query, "expected": expected_ids, "got": hyb_res})
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

        print(f"\nReal Gemini Hybrid Retriever Validation")
        print(f"=======================================")
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

        if false_negatives_log:
            print(f"False Negative Details:")
            for fn in false_negatives_log:
                print(f"  - Query: '{fn['query']}'")
                print(f"    Expected: {fn['expected']}, Got: {fn['got']}")

if __name__ == "__main__":
    run_evaluation()
