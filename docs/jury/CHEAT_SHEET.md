# ManakAI Jury Cheat Sheet

## 30-Second Pitch
"Navigating official BIS requirements is complex for small businesses and consumers. ManakAI is an independent, AI-assisted guidance prototype that translates natural language questions into structured, verified BIS compliance journeys. It simplifies the discovery process without replacing official BIS services, prioritizing safety and hallucination prevention over generative guessing."

## Architecture in 5 Lines
1. **User Query**: Accepts natural language input.
2. **Intent & Normalization**: Uses LLM only to normalize entities, not decide standards.
3. **Retrieval**: Uses hybrid semantic + deterministic keyword search against a verified knowledge base.
4. **Safety Gates**: Blocks vague queries, low-confidence matches, and unverified data.
5. **Decision**: Outputs evidence-backed answers (NO VERIFIED MATCH if uncertain).

## AI Role in 2 Lines
- The LLM is strictly a query normalizer (translating intent and language), **not** the decision-maker.
- Final standard selection is strictly deterministic and requires verified knowledge base evidence.

## Safety in 3 Lines
- **No Hallucinations**: Semantic similarity discovers candidates; deterministic gates prove applicability.
- **Vague Query Rejection**: Broad or ambiguous requests safely trigger a `NO VERIFIED MATCH`.
- **Verified Sources Only**: Every positive response cites and links directly to official BIS evidence.

## Differentiation in 2 Lines
- Unlike standard search, ManakAI understands intent and conversational context.
- Unlike generative AI, ManakAI is mathematically restricted from hallucinating legal requirements.

## 5 Key Numbers / Status Facts
- **Retrieval Safety Threshold**: 0.72 semantic minimum for non-ASCII matching.
- **Backend Tests Passing**: 72 automated regression/safety tests.
- **Live Normalization Verification**: 13/13 mocked validation cases passed (Gemini).
- **Core Technical Completion**: 90%
- **Knowledge Base Scope**: Curated prototype benchmark set; intentionally non-exhaustive.

## Top 10 Judge Questions & Answers
1. **Is ManakAI an LLM wrapper?** No. The LLM only normalizes queries. Decisions are deterministic.
2. **How do you prevent hallucinations?** By forbidding the LLM from selecting standards and requiring verifiable knowledge base evidence.
3. **What if the LLM fails?** The system safely falls back to native deterministic retrieval or rejects the query.
4. **Why not just use Google?** Google requires exact keyword knowledge; ManakAI understands intent and structures the compliance journey.
5. **Why not use the BIS website?** ManakAI acts as an accessible entry point to guide users *to* the correct BIS services.
6. **What is NO VERIFIED MATCH?** A deliberate safety feature that prevents guessing when evidence is insufficient.
7. **Is this an official BIS product?** No, it is an independent technology prototype.
8. **Why no massive vector database yet?** We prioritized deterministic safety and explainability over unchecked scale for this prototype phase.
9. **How do you handle multilingual queries?** Native semantic retrieval and LLM normalization (currently limited by upstream API quotas).
10. **Do you scrape BIS?** No. We use a verified, curated knowledge base to avoid hitting protected government systems.

## Exact Disclaimer
“ManakAI is an independent technology prototype providing AI-assisted guidance based on publicly available BIS information. For official decisions and services, please refer to BIS.”

## 3 Things NEVER to Claim
1. **Never claim** ManakAI is owned, approved, or endorsed by BIS.
2. **Never claim** the system possesses 100% real-world multilingual accuracy (due to API quotas).
3. **Never claim** ManakAI can make legally binding compliance decisions.
