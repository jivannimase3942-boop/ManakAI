# Phase 2E.3 Targeted Failure Analysis
**Date**: September 9, 2026

## 1. Executive Summary
This report analyzes the 15 failed queries from the 126-query Phase 2E.2 benchmark.

The evaluation was performed using the **`paraphrase-multilingual-MiniLM-L12-v2`** embedding model for the primary native semantic path. The secondary path (LLM Fallback) was triggered for all 15 failures but failed gracefully due to the Gemini API 429 Quota Exceeded error.

**Failure Breakdown (Total: 15)**
- **Hindi**: 7
- **Marathi**: 6
- **English**: 2

## 2. Root Cause Categories

### Category A: Multilingual Entity Gate (Score Thresholding)
**Count**: 13 failures (All Hindi & Marathi)
**Cause**: For non-ASCII queries, the system relies on a strict semantic override threshold (`>= 0.72`) to prove entity compatibility, since English keyword overlap is impossible.
- In **9 out of 13** cases, the native embedding successfully ranked the correct record as **#1**.
- However, the similarity scores ranged from `0.61` to `0.716` (e.g., *प्रेशर कुकर की सुरक्षा मानक क्या है?* scored `0.7165`).
- Because these scores fell just short of the conservative `0.72` safety gate, they were rejected as potentially unsafe matches.

### Category B: English Lexical Entity Gate (Vocabulary Gap)
**Count**: 2 failures (English Paraphrases)
**Cause**: The queries used product synonyms ("laptops", "notebooks") that are not explicitly present in the `kb-012` (IT Equipment) keywords or text.
- Even though the semantic score for "laptops" was incredibly high (`0.7812`), the strict deterministic requirement for lexical overlap (which prevents hallucinations) blocked the match.

## 3. Top-5 Ranking Performance (Native Semantic)
Despite failing the strict safety gates, the native embedding model showed strong retrieval capabilities:
- **Correct Candidate in Top-5**: 15 / 15 (100% of failed queries had the correct record in the top 5 candidates).
- **Correct Candidate Ranked #1**: 10 / 15 (66% of failed queries had the correct record ranked exactly #1).

## 4. LLM Fallback Status
- **LLM Fallback Attempted**: 15 / 15
- **LLM Fallback Unavailable**: 15 / 15 (429 Quota Exhausted)
*Note: The LLM fallback was designed specifically to rescue these exact queries by extracting English entities and bypassing the multilingual semantic limits. The safety architecture successfully blocked unsafe unverified matches when the LLM was down.*

## 5. Recommended Minimal Fixes
Do NOT make these fixes yet, pending review:

1. **For English Vocabulary Gaps (Category B)**: Add "laptops" and "notebooks" to the `keywords` array of `kb-012` in `knowledge_base.json`.
2. **For Multilingual Thresholds (Category A)**:
   - **Option 1 (Safest)**: Wait for the Gemini API quota to reset. The LLM normalization layer is already implemented to solve this exact problem by translating Hindi/Marathi products to English, guaranteeing lexical overlap.
   - **Option 2 (Tuning)**: Lower the non-ASCII semantic override threshold in `hybrid_retriever._check_product_compatibility` from `0.72` to `0.65`. This would immediately rescue most of the 13 queries, but risks increasing False Positives for out-of-domain queries.
