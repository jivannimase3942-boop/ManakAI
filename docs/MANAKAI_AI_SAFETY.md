# ManakAI AI Safety Model

## 1. Safety First Approach
ManakAI implements a defense-in-depth safety architecture. Because BIS standards have real-world legal and compliance consequences, preventing AI hallucinations is the system's highest priority.

## 2. Hallucination Prevention Guarantees
1. **Verified Retrieval Only**: The system strictly queries only verified knowledge records.
2. **State Filtering**: `PENDING`, `REJECTED`, or `SUPERSEDED` records are blocked from live retrieval deterministic logic.
3. **Evidence Thresholds**: A positive match is only returned when sufficient evidence exists in the verified database. Semantic similarity alone is never allowed to establish applicability.
4. **Vague Query Rejection**: Generic queries that lack sufficient product or service specificity are rejected by the safety gates.
5. **Domain Exclusivity**: Queries unrelated to BIS, product quality, or standard compliance are safely discarded.
6. **LLM Subordination**: The LLM operates strictly as a normalizer subordinate to deterministic validation gates. It can suggest a normalized query string, but it cannot override the database matching.

## 3. The "NO VERIFIED MATCH" Concept
When a query fails to meet the safety thresholds or targets a domain outside the verified knowledge base (e.g., "What BIS standard applies to aircraft certification?"), the system returns a safe, explicit `NO VERIFIED MATCH`.

**This is a deliberate safety outcome, NOT an application failure.**
It guarantees that ManakAI will never invent or guess a standard simply to provide a "helpful" answer. The frontend is designed to direct users back toward official BIS resources when this happens.

## 4. LLM Failure Handling
If the LLM normalization layer experiences failure (e.g., HTTP 429 quota exhaustion, prompt injection, malformed output), the system seamlessly falls back to the deterministic keyword/semantic retrieval path. A broken LLM guarantees a fallback, not a broken standard.
