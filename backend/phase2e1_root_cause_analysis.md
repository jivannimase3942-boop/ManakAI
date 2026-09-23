# Phase 2E.1 Root Cause Analysis

Based on diagnostic script execution (`diagnose_phase2e1.py`), here is the root cause analysis for the failures observed in the Phase 2E benchmark.

## A. Why Hindi/Marathi Semantic Retrieval is Failing
**Root Cause: ASCII-only Tokenization in Safety Gates**
Semantic retrieval (Gemini embeddings) works perfectly across languages. For example, the query "सीमेंट के लिए कौन सा BIS मानक लागू होता है?" correctly yields a semantic similarity of `0.7741` for the Cement record (`kb-011`).
However, it is rejected by the `_is_query_specific` gate (Gate 1.5) before hybrid scoring even begins. This is because the tokenization logic `re.findall(r"[a-z0-9]+", query.lower())` completely strips out non-ASCII scripts like Devanagari (Hindi) and Marathi. Thus, the system extracts zero product words and zero service words, incorrectly classifying the query as an ambiguous non-specific query and dropping it.

## B. Why `_check_product_compatibility` Rejects Multilingual Queries
For the same reason as above, if we fix the regex to include Unicode words (`r"\w+"`), `_get_product_words` would extract Hindi/Marathi tokens (e.g., "सीमेंट"). However, `_check_product_compatibility` expects to find these exact Hindi tokens in the English text (title, topic, keywords) of the knowledge base record. Since "सीमेंट" != "cement", this English lexical overlap check will inevitably fail and drop the candidate.

## C. Does Semantic Embedding Retrieve the Correct Record?
**Yes.** Gemini's cross-lingual embedding representation is highly accurate.
- "सीमेंट के लिए कौन सा BIS मानक लागू होता है?" -> `kb-011` (Sim: 0.7741)
- "सिमेंटसाठी कोणता BIS मानक लागू आहे?" -> `kb-011` (Sim: 0.7699)
In all multilingual test cases, the correct KB record is reliably identified by the embedding layer as the #1 candidate.

## D. Where Does the Failure Happen?
- **Hindi/Marathi**: Fails at **Gate 1.5** (`_is_query_specific`) due to ASCII-only tokenization.
- **English Paraphrases**: Fails at **Gate 2** (`Lexical Evidence`) or during **Hybrid Scoring**. If a valid paraphrase uses synonyms that have absolutely zero lexical overlap with the KB record, Gate 2 (`if not is_exact_id and kw_score == 0`) unilaterally drops the candidate, ignoring the high semantic similarity.

## E. Why do "where is the laboratory" and "how to apply" become False Positives?
**Root Cause: Service words bypassing the specificity gate**
In `hybrid_retriever.py`, "laboratory" and "apply" are designated as `SPECIFIC_SERVICE_WORDS`. The `_is_query_specific` gate allows queries with zero product words to pass if they contain a specific service word. Then, `_check_product_compatibility` defaults to `True` if there are no product words. Finally, because these generic service words exactly match the keywords/titles of `kb-004` (Laboratories) and `kb-002` (Product Certification), they achieve a non-zero `kw_score`. As a result, the generic service queries bypass all safety checks and are returned as confident matches, violating the requirement to return NO MATCH for underspecified intents.

## F. Why English Paraphrases ("drinking water testing") become False Negatives
**Root Cause: Over-strict product word extraction combined with Lexical Gate**
For "drinking water testing", the tokens are `{"drinking", "water", "testing"}`. "testing" is stripped as an intent stopword, leaving `{"drinking", "water"}`. However, `knowledge_base.search` (keyword search) assigns a score based on whole-phrase matching or exact word bounds. If `kw_score` evaluates to 0 (because the raw keyword search algorithm in `knowledge_base.py` didn't score it high enough without the exact phrase), Gate 2 instantly discards the candidate, despite the semantic similarity being a strong `0.6720`. Semantic matches with strong evidence are discarded merely because the lexical search engine failed to assign a `kw_score`.
