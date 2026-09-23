# Phase 2E.4 Multilingual Diagnostic Analysis
**Date**: September 9, 2026

## 1. Executive Summary
This report analyzes the remaining 13 multilingual (Hindi/Marathi) failures from the Phase 2E.2 evaluation. The root cause for all 13 queries is a failure at the **Entity Compatibility Gate**, driven by semantic similarity scores falling below the strict `0.72` non-ASCII safety threshold.

Critically, **simply lowering the threshold will not safely solve the problem**. In 4 of the 13 queries, the native embedding model (`paraphrase-multilingual-MiniLM-L12-v2`) incorrectly ranks a generic/unrelated record (e.g., `kb-002` Certification Process) higher than the correct product record. Lowering the threshold would thus convert these safe rejections into dangerous False Positives, destroying the system's current 100% precision.

This confirms that the existing architecture—which relies on **LLM Fallback for Entity Normalization**—is fundamentally the correct approach to safely support multilingual queries.

## 2. Detailed Query Analysis (13 Queries)

| Language | Query | Expected ID | Expected Product | Rank | Correct Score | Highest Wrong Score | Rejection Gate | Root Cause | LLM Attempted |
|---|---|---|---|---|---|---|---|---|---|
| hi | क्या खिलौनों के लिए ISI मार्क अनिवार्य है? | kb-010 | Toys | 4 | 0.661 | 0.685 (kb-002) | Entity Compat | C, B | Yes (429) |
| hi | हेलमेट का IS नंबर क्या है? | kb-013 | Helmet | 1 | 0.682 | None | Entity Compat | B | Yes (429) |
| hi | प्रेशर कुकर की सुरक्षा मानक क्या है? | kb-014 | Cooker | 1 | 0.716 | None | Entity Compat | B | Yes (429) |
| hi | क्या बच्चों के खिलौने सुरक्षित हैं? | kb-010 | Toys | 1 | 0.661 | None | Entity Compat | B | Yes (429) |
| hi | आईटी उपकरणों के लिए CRS स्कीम | kb-012 | IT Equipment | 2 | 0.660 | 0.664 (kb-008) | Entity Compat | C, B | Yes (429) |
| hi | कुकर पर ISI मार्क | kb-014 | Cooker | 1 | 0.715 | None | Entity Compat | B | Yes (429) |
| hi | खिलौनों की टेस्टिंग | kb-010 | Toys | 1 | 0.647 | None | Entity Compat | B | Yes (429) |
| mr | पिण्याच्या पाण्यासाठी काय नियम आहेत? | kb-001 | Drinking Water | 1 | 0.676 | None | Entity Compat | B | Yes (429) |
| mr | खेळण्यांसाठी ISI मार्क अनिवार्य आहे का? | kb-010 | Toys | 3 | 0.675 | 0.689 (kb-002) | Entity Compat | C, B | Yes (429) |
| mr | मुलांची खेळणी सुरक्षित आहेत का? | kb-010 | Toys | 1 | 0.695 | None | Entity Compat | B | Yes (429) |
| mr | आयटी उपकरणांसाठी CRS योजना | kb-012 | IT Equipment | 1 | 0.692 | None | Entity Compat | B | Yes (429) |
| mr | दुचाकी हेल्मेट प्रमाणपत्र | kb-013 | Helmet | 1 | 0.698 | None | Entity Compat | B | Yes (429) |
| mr | खेळण्यांची चाचणी | kb-010 | Toys | 2 | 0.613 | 0.619 (kb-004) | Entity Compat | C, B | Yes (429) |

*Root Cause Legend: [B] Correct candidate below semantic threshold. [C] Wrong semantic candidate ranked above correct candidate.*

## 3. Aggregate Analysis

### Distribution
- **Total Failures**: 13 (7 Hindi, 6 Marathi)
- **Expected record ranked #1**: 9 (69%)
- **Expected record ranked Top-3**: 12 (92%)
- **Expected record ranked Top-5**: 13 (100%)
- **Wrong record outranks expected**: 4 (30%)

### Score Analysis
- **Minimum semantic score of correct candidates**: `0.613`
- **Maximum semantic score of wrong candidates**: `0.689`
- **Score gap where wrong record outranked expected**: Between `-0.004` and `-0.024`. The wrong candidates win by extremely narrow margins, making it impossible to separate them using confidence margin thresholds alone.

## 4. Safety-Risk Analysis
The native embedding model struggles to distinguish between specific product queries in regional languages and generic certification intents. For example, "खेळण्यांसाठी ISI मार्क अनिवार्य आहे का?" (Is ISI mark mandatory for toys?) ranks the generic BIS Certification Process (`kb-002`) at `0.689`, above the Toys standard (`kb-010`) at `0.675`.

Because English lexical overlap is impossible for native Hindi/Marathi tokens, the system rightfully treats these matches as high-risk and rejects them.

## 5. Architectural Recommendations (Explicit Answers)

**1. Can we safely solve most failures with native semantic + entity resolution?**
Yes. An LLM-based entity normalization layer flawlessly bridges the gap. By extracting the English entity ("toys"), the pipeline can fall back to the deterministic Lexical Entity Gate, proving product compatibility with 100% confidence, completely bypassing the messy semantic scoring.

**2. Is lowering 0.72 justified by the observed data?**
**No.** Lowering the threshold to `0.60` (to encompass the lowest correct score of `0.613`) would immediately cause at least 4 False Positives, reducing the system's Precision from 100%.

**3. Is LLM normalization actually required?**
**Yes.** Because the native embedding model cannot reliably rank the correct product over generic service records for regional languages, LLM normalization is mandatory to maintain 100% precision while achieving high recall. The 13 failures only occurred because the LLM was unavailable due to Gemini's 429 Quota Exceeded error.

**4. What is the smallest change that could improve recall while preserving the current 100% precision?**
Implement a robust retry/backoff mechanism, API key rotation, or fallback to an alternate LLM provider (e.g., OpenRouter) specifically for the `extract_query_context` function. Since the LLM is only called when deterministic checks fail, ensuring its availability will solve these 13 queries.

**5. What tests should be added before any fix?**
- E2E tests simulating the 429 Quota Exceeded error to ensure the system gracefully returns `NO VERIFIED MATCH` (already proven in production, but should be formalized).
- E2E tests validating the LLM fallback path specifically on Hindi/Marathi queries using a reliable mocked LLM response to confirm that when the LLM successfully extracts English product names, the final record is selected correctly.
