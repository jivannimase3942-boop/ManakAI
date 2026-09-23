# Phase 2E.1 Multilingual Architecture Options

This document analyzes the viability of multilingual semantic retrieval based on diagnostic tests, and compares three architectural approaches for ManakAI.

## Diagnostic Findings: Native Multilingual Embeddings

We tested the Gemini embedding model by feeding raw Hindi and Marathi queries and evaluating whether it could retrieve the corresponding English BIS records directly.

**Results:**
- **Hindi - Cement:** Rank 1 (`kb-011`, Sim: 0.7746) ✅
- **Marathi - Cement:** Rank 1 (`kb-011`, Sim: 0.7699) ✅
- **Hindi - Packaged Drinking Water:** Rank 1 (`kb-001`, Sim: 0.7767) ✅
- **Marathi - Packaged Drinking Water:** Rank 1 (`kb-001`, Sim: 0.8217) ✅
- **Marathi - Toys:** Rank 4 (`kb-010`, Sim: 0.6883) ✅
- **Hindi - Toys:** Did not appear in Top 5 (Sim < 0.66) ❌
- **Hindi - Aircraft Certification (Unsupported):** Rank 1 (`kb-002`, Sim: 0.5661) (Safely below 0.65 threshold) ✅

**Conclusion on Native Embeddings:**
The multilingual embeddings are **highly capable** and can directly map many non-English queries to English KB records without translation. However, they are not perfect (e.g., Hindi "toys" suffered from lower recall). Relying purely on semantic search would cause a slight regression in recall for less common vocabulary.

---

## Architecture Comparisons

### A. LLM Normalization on Every Multilingual Query (Current Implementation)
*How it works:* All non-ASCII queries are passed to the LLM for English translation and entity extraction before retrieval.
- **Accuracy Potential:** Highest (LLM handles complex linguistic nuances and extracts clean entities).
- **Latency:** Very High (~12 seconds per non-ASCII query due to rate limiting, or ~2-3s without rate limiting).
- **API Dependency:** 100% dependency on the Generative LLM API for non-English queries.
- **Quota Risk:** Extreme (Exhausts free-tier daily quotas extremely quickly).
- **Scalability:** Poor (Costly and slow at scale).
- **Safety:** High (Fallback defaults to NO MATCH if the LLM fails).
- **Implementation Complexity:** Moderate.

### B. Pure Multilingual Semantic Retrieval (No LLM Normalization)
*How it works:* Remove the LLM normalizer entirely. Rely on the embedding model's native cross-lingual capabilities.
- **Accuracy Potential:** Moderate (Works well for common terms like "Cement", but misses some translations like Hindi "Toys").
- **Latency:** Extremely Low (< 200ms).
- **API Dependency:** Only relies on the Embedding API (much higher quota limits, 1500 req/day).
- **Quota Risk:** Low.
- **Scalability:** Excellent.
- **Safety:** High (The semantic threshold of `0.65` safely filters out out-of-domain queries like "aircraft certification"). However, the structural "vague query" gate (Gate 1.2) would need to be redesigned, as `_get_product_words` strips non-ASCII characters, which would falsely flag all valid Hindi/Marathi queries as vague.
- **Implementation Complexity:** Low.

### C. Hybrid Fallback Approach (Recommended)
*How it works:* Treat native Multilingual Semantic Retrieval as the **Primary Path** for all queries. Only use the LLM normalizer as a **Secondary Fallback Path** when the primary path yields low confidence or no matches.
- **Accuracy Potential:** Highest (Combines the speed of native embeddings with the fallback intelligence of the LLM).
- **Latency:** Extremely Low for most queries (< 200ms). High only for edge cases requiring the LLM.
- **API Dependency:** Minimal LLM usage.
- **Quota Risk:** Very Low (LLM is only triggered for a small fraction of queries).
- **Scalability:** Excellent.
- **Safety:** High. If the LLM quota is exhausted, the system simply relies on the native semantic retrieval.
- **Implementation Complexity:** High (Requires two-stage retrieval logic).

---

## Recommended Architecture: C. Hybrid Fallback Approach

We recommend implementing **Option C**.

### Implementation Plan:
1. **Primary Path (Deterministic + Native Semantic):**
   - Execute the standard hybrid retrieval (Lexical + Semantic) using the raw multilingual query.
   - **Fix Vague Query Gate:** Update `_get_product_words()` to retain non-ASCII characters (e.g., `re.findall(r"[^\W_]+", query)`) so that valid Hindi/Marathi queries aren't falsely rejected as vague.
   - If a valid match is found that satisfies all safety gates (Score >= Threshold), return it immediately (0 LLM latency).
2. **Secondary Path (LLM Normalization):**
   - If the primary path yields NO MATCH, **and** the query contains non-ASCII characters, **and** the LLM quota is available, trigger `extract_query_context()` to translate the query.
   - Re-run the standard retrieval using the translated English query.
3. **Safety Guarantee:** If the LLM rate limits or fails on the secondary path, the system simply returns the NO MATCH result from the primary path, preserving 100% safety.
