# ManakAI System Limitations

While ManakAI successfully demonstrates a highly secure, hallucination-resistant architecture for BIS compliance guidance, several limitations exist within the current prototype scope:

## 1. Knowledge Base Scale
- The current knowledge base is heavily curated and verified for the SIH 2026 demonstration. It is **not exhaustive** and does not contain all thousands of BIS standards.
- Full BIS standard documents (PDFs) are **not** indiscriminately downloaded, parsed, or vectorized due to copyright protections and unnecessary retrieval noise.

## 2. External System Integration
- Some BIS databases (like licensed laboratories or dynamic fee tables) are protected or dynamic. ManakAI does **not** scrape these systems in real-time, relying instead on scheduled, verified ingestion pipelines.
- Official BIS decisions, application approvals, and standard updates remain entirely outside the scope of ManakAI.

## 3. API Quotas
- LLM normalization heavily depends on the availability of the upstream provider (Gemini API).
- Live multilingual validation currently faces constraints due to external HTTP 429 Quota Exhaustion. While the system safely falls back to native English retrieval when this occurs, true 100% automated multilingual parsing is bound by API limits.

## 4. UI Validation
- The frontend UI utilizes robust structural rendering (`DecisionCard`, `NoVerifiedMatch`) confirmed by static analysis and DOM generation. However, exhaustive cross-browser pixel-perfect visual validation remains a post-prototype effort.
