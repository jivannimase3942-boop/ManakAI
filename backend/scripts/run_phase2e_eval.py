import json
import os
import sys
import time
from typing import Dict, Any

# Ensure backend is in PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

# We MUST NOT bypass rag.py
from app import rag
from app import knowledge_base

def run_evaluation():
    sys.stdout.reconfigure(encoding='utf-8')
    eval_dir = os.path.join(os.path.dirname(__file__), "..", "evaluation")
    benchmark_path = os.path.join(eval_dir, "phase2e_benchmark.json")

    with open(benchmark_path, "r", encoding="utf-8") as f:
        benchmark = json.load(f)

    all_kb_records = knowledge_base.all_records()
    title_to_id = {r["title"]: r["id"] for r in all_kb_records}

    results = []

    metrics = {
        "Total": len(benchmark),
        "Correct": 0,
        "Incorrect": 0,
        "TP": 0,
        "TN": 0,
        "FP": 0,
        "FN": 0,
        "Infrastructure_Failures": 0
    }

    category_metrics = {}
    language_metrics = {}

    failed_queries = []

    from scripts.identity_helper import matches_expected_identity

    print(f"Running Phase 2E Evaluation on {len(benchmark)} queries...")
    print(f"USE_HYBRID_RETRIEVAL = {rag.USE_HYBRID_RETRIEVAL}")

    start_time = time.time()

    for case in benchmark:
        query = case["query"]
        expected_match = case["expected_match"]
        expected_record_id = case["expected_record_id"]

    def evaluate_case(case: Dict[str, Any]) -> float:
        cat = case["category"]
        lang = case["language"]

        if cat not in category_metrics:
            category_metrics[cat] = {"Total": 0, "Correct": 0}
        if lang not in language_metrics:
            language_metrics[lang] = {"Total": 0, "Correct": 0}

        category_metrics[cat]["Total"] += 1
        language_metrics[lang]["Total"] += 1

        import io
        import contextlib

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            t0 = time.time()
            result = rag.find_standard_for_product(case["query"], language=case["language"])
            t1 = time.time()

        output = f.getvalue()
        sys.stdout.write(output)
        latency = t1 - t0

        if "LLM Extraction failed" in output or "429 You exceeded" in output:
            metrics["Infrastructure_Failures"] += 1
            metrics["Total"] -= 1 # Do not count towards accuracy
            category_metrics[cat]["Total"] -= 1
            language_metrics[lang]["Total"] -= 1
            failed_queries.append({
                "case": case,
                "reason": "evaluation_infrastructure_failure",
                "predicted_record_id": None,
                "predicted_standard_number": None,
                "latency": latency
            })
            return latency

        predicted_record = result["sources"][0] if result and result.get("sources") else None
        predicted_record_id = predicted_record.get("id") if predicted_record else None
        predicted_std_num = predicted_record.get("standard_number") if predicted_record else None

        is_correct = False
        if case["expected_match"]:
            is_correct = matches_expected_identity(case, predicted_record)
        else:
            if predicted_record_id is None:
                is_correct = True

        if is_correct:
            metrics["Correct"] += 1
            category_metrics[cat]["Correct"] += 1
            language_metrics[lang]["Correct"] += 1

            if case["expected_match"]:
                metrics["TP"] += 1
            else:
                metrics["TN"] += 1
        else:
            metrics["Incorrect"] += 1
            if case["expected_match"]:
                metrics["FN"] += 1
            else:
                metrics["FP"] += 1

            failed_queries.append({
                "case": case,
                "predicted_record_id": predicted_record_id,
                "predicted_standard_number": predicted_std_num,
                "latency": latency
            })

        return latency

    latencies = []
    for case in benchmark:
        lat = evaluate_case(case)
        latencies.append(lat)
        # Sleep to avoid hitting Gemini's 15 RPM free tier rate limit
        time.sleep(4.1)

    end_time = time.time()

    tp = metrics["TP"]
    tn = metrics["TN"]
    fp = metrics["FP"]
    fn = metrics["FN"]

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    metrics["Accuracy"] = metrics["Correct"] / metrics["Total"] if metrics["Total"] > 0 else 0
    metrics["Precision"] = precision
    metrics["Recall"] = recall
    metrics["F1"] = f1

    import numpy as np
    p50_latency = np.percentile(latencies, 50)
    p95_latency = np.percentile(latencies, 95)
    avg_latency = np.mean(latencies)

    print(f"Evaluation completed in {end_time - start_time:.2f} seconds.")
    print(f"\nLATENCY: p50={p50_latency:.3f}s | p95={p95_latency:.3f}s | avg={avg_latency:.3f}s\n")

    # Print Summary
    print("\n" + "="*50)
    print("OVERALL METRICS")
    print("="*50)
    print(f"Total Queries : {metrics['Total']}")
    print(f"Correct       : {metrics['Correct']}")
    print(f"Incorrect     : {metrics['Incorrect']}")
    print(f"Accuracy      : {metrics['Accuracy']:.2%}")
    print(f"Precision     : {precision:.2%}")
    print(f"Recall        : {recall:.2%}")
    print(f"F1 Score      : {f1:.2%}")
    print(f"True Positive : {tp}")
    print(f"True Negative : {tn}")
    print(f"False Positive: {fp}")
    print(f"False Negative: {fn}")

    print("\n" + "="*50)
    print("CATEGORY ACCURACY")
    print("="*50)
    for cat, m in category_metrics.items():
        acc = m["Correct"] / m["Total"] if m["Total"] > 0 else 0
        print(f"{cat.ljust(15)}: {m['Correct']}/{m['Total']} ({acc:.2%})")

    print("\n" + "="*50)
    print("LANGUAGE ACCURACY")
    print("="*50)
    for lang, m in language_metrics.items():
        acc = m["Correct"] / m["Total"] if m["Total"] > 0 else 0
        print(f"{lang.ljust(15)}: {m['Correct']}/{m['Total']} ({acc:.2%})")

    print("\n" + "="*50)
    print(f"FAILED QUERIES ({len(failed_queries)})")
    print("="*50)

    from app import llm, intent
    from app.semantic_retriever import get_semantic_candidates

    for fq in failed_queries:
        case = fq["case"]
        query = case['query']
        print(f"Query: {case['query']}")
        print(f"Expected: Match={case['expected_match']}, ID={case['expected_record_id']}")
        pred_id = fq.get("predicted_record_id")
        print(f"Actual: Match={pred_id is not None}, ID={pred_id}")

        if fq.get("reason") == "evaluation_infrastructure_failure":
            print("  -> FAILURE REASON: evaluation_infrastructure_failure (Rate Limit)")
            print("-" * 30)
            continue

        # Diagnostic Info
        norm_context = llm.extract_query_context(query)
        print(f"  -> Extracted Entity: {norm_context.get('product_entity_en')}")
        print(f"  -> Is Generic: {norm_context.get('is_generic')}")
        norm_query_en = norm_context.get("normalized_query_en") or query.lower()
        print(f"  -> Detected Intent: {intent.detect_intent(norm_query_en)}")

        sem_cands = get_semantic_candidates(query, top_k=1)
        if sem_cands:
            top_cand = sem_cands[0]
            print(f"  -> Top Semantic Cand: {top_cand['record_id']} (Sim: {top_cand['similarity']:.4f})")
        print("-" * 30)

    # Save results to a file for reporting
    results_path = os.path.join(eval_dir, "phase2e_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump({
            "metrics": metrics,
            "category_metrics": category_metrics,
            "language_metrics": language_metrics,
            "failed_queries": failed_queries,
            "latency": {
                "p50": p50_latency,
                "p95": p95_latency,
                "avg": avg_latency
            }
        }, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    run_evaluation()
