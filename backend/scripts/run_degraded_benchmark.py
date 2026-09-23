import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["GEMINI_API_KEY"] = "FAKE"

from app.hybrid_retriever import hybrid_search
from scripts.identity_helper import matches_expected_identity

benchmark = json.load(open('evaluation/phase2e_benchmark.json', encoding='utf-8'))

# Pick 3 of each category
categories = ['valid', 'hindi', 'marathi', 'generic', 'adversarial', 'exact_id']
selected = []
counts = {c: 0 for c in categories}
for case in benchmark:
    cat = case.get('category')
    if cat in counts and counts[cat] < 3:
        selected.append(case)
        counts[cat] += 1

correct = 0
incorrect = 0
no_match = 0
fp = 0
fn = 0

for case in selected:
    q = case['query']

    # Run hybrid search directly
    records = hybrid_search(q, top_k=1)
    pred_record = records[0] if records else None
    pred_id = pred_record.get('id') if pred_record else None

    expected_match = case['expected_match']

    if not expected_match:
        if pred_id is None:
            correct += 1
        else:
            incorrect += 1
            fp += 1
    else:
        if pred_id is None:
            no_match += 1
            fn += 1
        else:
            if matches_expected_identity(case, pred_record):
                correct += 1
            else:
                incorrect += 1
                fp += 1

print("\n--- RESULTS ---")
print(f"Total Evaluated: {len(selected)}")
print(f"Correct (or safely rejected): {correct}")
print(f"NO VERIFIED MATCH (Degraded Safety): {no_match}")
print(f"Incorrect: {incorrect}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")
