# ManakAI Data Flow

## 1. Information Retrieval Pipeline

The core data flow in ManakAI is designed to extract meaning from user intent and firmly attach it to official, verified BIS data structures.

1. **User Query Input**: The raw text, regardless of language, arrives at the application layer.
2. **Intent Parsing**: The query passes through the `intent.py` engine, evaluating whether the user is seeking `REQUIREMENTS`, `CERTIFICATION`, `TESTING`, etc.
3. **Optional LLM Normalization**: For complex or multilingual queries, the LLM converts the unstructured string into a structured entity mapping (`normalized_query`). If this step fails, it is bypassed.
4. **Candidate Retrieval (`knowledge_base.py` / `semantic_retriever.py`)**:
   - The system retrieves all theoretically relevant candidates via semantic embeddings and deterministic keyword overlaps.
5. **Safety Filtering (`hybrid_retriever.py`)**:
   - The top candidates are passed through strict entity and state filters.
6. **Decision Processing (`decision.py`)**:
   - A singular verified match is selected if it clears the hybrid safety score threshold. If no candidates pass, a `NO VERIFIED MATCH` payload is generated.
7. **Payload Delivery (`models.py`)**:
   - The system serializes the decision, associated `requirements`, `testing` parameters, `certification_steps`, and `sources` into the robust `ComplianceResponse` schema.
8. **UI Presentation (`frontend/`)**:
   - `ChatMessage.jsx` dispatches the JSON payload to the appropriate structural view (`DecisionCard` or `NoVerifiedMatch`), maintaining strict transparency through the `WhyThisAnswer` explanation block.
