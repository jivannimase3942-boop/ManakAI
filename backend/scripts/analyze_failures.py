import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["USE_HYBRID_RETRIEVAL"] = "true"
from dotenv import load_dotenv
load_dotenv()

from app import hybrid_retriever
from app import semantic_retriever

def analyze_failures():
    with open('evaluation/phase2e_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)

    failed = results['failed_queries']

    analysis = []

    for f in failed:
        case = f["case"]
        query = case["query"]
        lang = case["language"]
        expected_id = case["expected_record_id"]

        sem_cands = semantic_retriever.get_semantic_candidates(query, top_k=5)

        # Capture raw scoring details from hybrid_retriever logic
        # Because hybrid_search sorts and filters, we will temporarily capture all records before filtering
        # To do this safely, we will just call hybrid_search and see what it returns, and manually simulate the gates

        expected_rec = None
        for r in hybrid_retriever.knowledge_base.all_records():
            if r["id"] == expected_id:
                expected_rec = r
                break

        is_exact_id = False
        if expected_rec:
            std_num = expected_rec.get("standard_number", "").lower()
            if std_num and len(std_num) > 3 and std_num in query.lower():
                is_exact_id = True

        is_non_ascii = any(ord(c) >= 128 for c in query)
        is_vague = not hybrid_retriever._is_query_specific(query, is_exact_id)

        # To get the exact score for the expected record:
        exp_sem_score = 0.0
        for c in sem_cands:
            if c["record_id"] == expected_id:
                exp_sem_score = c["similarity"]
                break
        if exp_sem_score == 0.0:
            all_sem_cands = semantic_retriever.get_semantic_candidates(query, top_k=20)
            for c in all_sem_cands:
                if c["record_id"] == expected_id:
                    exp_sem_score = c["similarity"]
                    break

        ent_compat = False
        intent_compat = False
        if expected_rec:
            ent_compat = hybrid_retriever._check_product_compatibility(query, expected_rec, exp_sem_score, is_non_ascii)
            from app import intent
            query_intent = intent.detect_intent(query)
            intent_compat = hybrid_retriever._check_intent_compatibility(query_intent, expected_rec)

        analysis.append({
            "query": query,
            "language": lang,
            "expected_id": expected_id,
            "top_5_sem": sem_cands,
            "is_non_ascii": is_non_ascii,
            "is_vague": is_vague,
            "expected_sem_score": exp_sem_score,
            "ent_compat": ent_compat,
            "intent_compat": intent_compat,
        })

    with open('evaluation/failure_analysis_raw.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    analyze_failures()
