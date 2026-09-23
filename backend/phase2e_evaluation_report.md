# Phase 2E Evaluation Report

## Dataset
- **Total Queries**: 126
- **Category Counts**:
  - Valid Product Queries: 30
  - Paraphrased Valid Queries: 21
  - Exact Standard-ID Queries: 10
  - Generic / Underspecified Queries: 15
  - Cross-Domain / Adversarial Queries: 20
  - Hindi Queries: 15
  - Marathi Queries: 15
- **Industry/Consumer Counts**:
  - Industry: 104
  - Consumer: 22

## Overall Metrics
- **Accuracy**: 62.70%
- **Precision**: 95.83%
- **Recall**: 50.55%
- **F1 Score**: 66.19%
- **True Positives (TP)**: 46
- **True Negatives (TN)**: 33
- **False Positives (FP)**: 2
- **False Negatives (FN)**: 45

## Category Metrics
| Category | Correct / Total | Accuracy |
|----------|-----------------|----------|
| Valid | 22 / 30 | 73.33% |
| Paraphrase | 10 / 21 | 47.62% |
| Exact ID | 10 / 10 | 100.00% |
| Generic | 13 / 15 | 86.67% |
| Adversarial | 20 / 20 | 100.00% |
| Hindi | 2 / 15 | 13.33% |
| Marathi | 2 / 15 | 13.33% |

## Safety Results
- **Generic Rejection Rate**: 86.67% (13/15 correct)
- **Adversarial Rejection Rate**: 100.00% (20/20 correct)
- **False Positives**: 2
- **False Negatives**: 45
The system shows exceptional safety against cross-domain hallucinations (0 adversarial matches). However, the generic rejection failed on two queries due to missing stop words.

## Multilingual Results
- **Hindi Accuracy**: 13.33% (2/15)
- **Marathi Accuracy**: 13.33% (2/15)
The retrieval pipeline severely underperforms on non-English queries, failing to route valid user queries to the correct records.

## Failed Queries (Sample)
A total of 47 queries failed. Below are representative examples with root cause analysis.

### False Positives (Failed to reject)
1. **Query**: "where is the laboratory"
   - **Expected**: No Match
   - **Actual**: `kb-004` (BIS-Recognised Testing Laboratories)
   - **Root Cause**: The word "laboratory" is not listed in `INTENT_STOPWORDS`. The safety gate treated it as a specific product, and since it matches `kb-004` exactly, it passed. (Data Coverage / Gate configuration issue)
2. **Query**: "how to apply"
   - **Expected**: No Match
   - **Actual**: `kb-002` (Product Certification Scheme)
   - **Root Cause**: "apply" is not an intent stopword, causing a keyword match to `kb-002`.

### False Negatives (Failed to retrieve)
3. **Query**: "drinking water testing"
   - **Expected**: `kb-001` (IS 14543)
   - **Actual**: No Match
   - **Root Cause**: Retrieval thresholding. While semantic matching might find the record, the strict product verification loop or the score threshold (`MIN_HYBRID_SCORE=0.25`) rejected the match. (Retrieval Tuning issue)
4. **Query**: "toy safety testing"
   - **Expected**: `kb-010`
   - **Actual**: No Match
   - **Root Cause**: Similar to above, product keywords "toy safety" may not sufficiently cross the strict compatibility gates or semantic score threshold.
5. **Query**: "सीमेंट के लिए कौन सा BIS मानक लागू होता है?" (Hindi)
   - **Expected**: `kb-011`
   - **Actual**: No Match
   - **Root Cause**: The `_check_product_compatibility` gate relies on English substring matching (`query.lower()`) against the English KB fields. It cannot verify product alignment for Hindi tokens (Language Handling issue).

## Final Assessment
**Class C. NOT READY**

While the safety against cross-domain hallucinations is perfect (100%), the system is heavily biased towards English exact-keyword matching. It currently lacks the necessary multilingual product matching logic and has an overly strict threshold that drops valid paraphrased English queries. The false positive cases on generic queries also reveal that the hardcoded `INTENT_STOPWORDS` list is brittle. The architecture must address language handling and robust intent/product separation before Phase 3.
