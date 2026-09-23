import os
import sys
import json
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app import knowledge_base
from app.semantic_retriever import get_semantic_candidates
from app.hybrid_retriever import hybrid_search, _get_product_words, _check_product_compatibility, _is_query_specific
from google import genai
import app.embeddings as embeddings

# Force stdout encoding to utf-8 for Hindi/Marathi
sys.stdout.reconfigure(encoding='utf-8')

# Ensure API Key is loaded
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    embeddings._CLIENT = genai.Client(api_key=api_key)

def diagnose_queries():
    eval_dir = os.path.join(os.path.dirname(__file__), "..", "evaluation")
    benchmark_path = os.path.join(eval_dir, "phase2e_benchmark.json")

    with open(benchmark_path, "r", encoding="utf-8") as f:
        benchmark = json.load(f)

    # We only care about failed Hindi, Marathi, and Paraphrase cases, plus the 2 false positives
    failed_cases = []

    print("=== MULTILINGUAL / PARAPHRASE DIAGNOSTIC ===\n")

    for case in benchmark:
        # Check false positives
        if case["query"] in ["where is the laboratory", "how to apply"]:
            failed_cases.append(case)
        # Check some hindi/marathi failures
        elif case["language"] in ["hi", "mr"] and case["expected_match"]:
            failed_cases.append(case)
        # Check some paraphrase failures
        elif case["category"] == "paraphrase" and case["expected_match"] and case["query"] in ["drinking water testing", "toy safety testing"]:
            failed_cases.append(case)

    # Let's just limit to a few illustrative examples for the report
    targets = [
        "aircraft certification",
        "certification",
        "drinking water testing",
        "where is the laboratory",
        "how to apply",
        "सीमेंट के लिए कौन सा BIS मानक लागू होता है?",
        "सिमेंटसाठी कोणता BIS मानक लागू आहे?"
    ]

    for case in benchmark:
        query = case["query"]
        if query not in targets:
            continue

        print("="*60)
        print(f"QUERY: {query} (Lang: {case['language']})")
        print("="*60)

        # 1. Semantic Candidates
        sem_cands = get_semantic_candidates(query, top_k=5)
        print(f"\n[1] SEMANTIC CANDIDATES (Top 5):")
        sem_map = {}
        all_kb_records = {r["id"]: r for r in knowledge_base.all_records()}
        for sc in sem_cands:
            record = all_kb_records.get(sc["record_id"])
            if record:
                title = record.get("title", "")
                std = record.get("standard_number", "")
                sem_map[sc["record_id"]] = sc["similarity"]
                print(f"  -> {sc['record_id']} | {std} | {title} | Sim: {sc['similarity']:.4f}")

        # 2. Gate Diagnostics
        print(f"\n[2] GATE DIAGNOSTICS:")
        product_words = _get_product_words(query)
        print(f"  -> Extracted Product Words: {product_words}")
        is_spec = _is_query_specific(query, False)
        print(f"  -> Passes _is_query_specific?: {is_spec}")

        # 3. Product Compatibility for expected record
        expected_rid = case["expected_record_id"]
        if expected_rid:
            expected_rec = all_kb_records.get(expected_rid)
            compat = _check_product_compatibility(query, expected_rec)
            print(f"  -> _check_product_compatibility for {expected_rid}: {compat}")
            if not compat:
                record_text = (expected_rec.get("title", "") + " " + expected_rec.get("topic", "") + " " + " ".join(expected_rec.get("keywords", []))).lower()
                print(f"     (Record text was: {record_text})")

        # 4. Hybrid Search output
        print(f"\n[3] HYBRID SEARCH OUTPUT:")
        hyb_results = hybrid_search(query, top_k=3)
        if hyb_results:
            for hr in hyb_results:
                print(f"  -> MATCH: {hr['id']} | Score: {hr.get('_hybrid_score')}")
        else:
            print("  -> MATCH: [] (Rejected by gates or score threshold)")

        print("\n")

if __name__ == "__main__":
    diagnose_queries()
