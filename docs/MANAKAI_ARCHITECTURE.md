# ManakAI Architecture

## 1. Overview
ManakAI is an independent technology prototype providing AI-assisted guidance based on publicly available BIS information. For official decisions and services, please refer to BIS.

The architecture is built heavily around deterministic safety, separating AI (LLM) intent-normalization from final authoritative retrieval and compliance logic.

## 2. Core System Components

- **Frontend (React + Vite)**: A lightweight, evidence-driven public service interface utilizing clear structural displays (`DecisionCard`, `WhyThisAnswer`, `EvidencePanel`, `ComplianceJourney`).
- **Backend API (FastAPI)**: A high-performance Python application handling stateless querying.
- **Intent Engine**: Parses user input deterministically into workflows (e.g., REQUIREMENTS, CERTIFICATION).
- **Retrieval Engine**:
  - *Lexical/Keyword Retrieval*: High-precision baseline fallback.
  - *Semantic Embeddings*: Captures natural language semantic intent (e.g., multilingual, typographical variance).
- **LLM Normalizer Layer**: Processes ambiguous or multilingual inputs safely by converting unstructured context into structured query inputs (normalized query strings) ONLY. It does *not* make BIS applicability decisions.
- **Decision Engine**: Combines intents and retrieved verified records, passing them through rigorous safety gates to construct a `ComplianceResponse`.

## 3. High-Level Flow
1. **User Query**: Input via standard API or Chat.
2. **Query Normalization (Optional LLM)**: Entity extraction, language normalization.
3. **Intent Detection**: Rule-based detection.
4. **Retrieval Strategy**:
   - Deterministic Keyword Retrieval + Semantic Retrieval (Hybrid approach).
5. **Candidate Gating**: Filters invalid, unverified, PENDING, REJECTED, or SUPERSEDED records.
6. **Hybrid Ranking**: Balances vector similarity with exact entity matches.
7. **Safety / Confidence Gate**: Validates whether the matched candidate crosses the minimum acceptable threshold for generic safety.
8. **Deterministic Decision Engine**: Constructs the final payload.
9. **Evidence-backed Compliance Response**: Payload sent to UI.
10. **Frontend Display**: `DecisionCard`, `WhyThisAnswer`, `EvidencePanel`, and `ComplianceJourney`.

## 4. LLM Role & Boundaries
The LLM is strictly positioned as a **Normalization Layer**.
- **What it does**: Outputs structured fields like `normalized_query`, `product_entity`, `service_entity`.
- **What it does NOT do**: It does not perform internal searches, generate fake URLs, or make decisions on which BIS standard applies.
- **Fallback**: If the LLM returns malformed output, times out, hits HTTP 429 quota exhaustion, or fails confidence checks, the system deterministically falls back to the native hybrid keyword/semantic search to prevent catastrophic failure.
