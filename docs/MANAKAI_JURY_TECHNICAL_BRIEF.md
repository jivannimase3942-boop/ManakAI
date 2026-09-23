# ManakAI Jury Technical Brief

## Problem
Navigating official BIS (Bureau of Indian Standards) requirements is complex. Small manufacturers, importers, and consumers often struggle to map their specific product to the correct bureaucratic standard, testing requirement, or certification scheme using traditional keyword searches.

## Solution
ManakAI does **not** replace official BIS services. Instead, it radically simplifies the journey to the right BIS service. It acts as an independent, AI-assisted guidance prototype that translates natural language questions into structured, verified BIS compliance journeys.

## Architecture
- **Frontend**: Evidence-driven React + Vite SPA prioritizing transparency and trust.
- **Backend**: High-performance FastAPI Python engine executing deterministic matching.
- **Knowledge Base**: Curated, strictly verified JSON repository of official BIS rules and requirements.

## AI Role & Safety Mechanism
The most critical architectural feature of ManakAI is its **defense-in-depth safety model**.
1. **Retrieval Strategy**: Uses hybrid semantic and keyword retrieval to cast a wide net for potential matches.
2. **AI Role**: The LLM is used **strictly for query normalization** (e.g., entity extraction, intent detection, translating multilingual input). It NEVER independently selects a standard.
3. **Safety Mechanism**: Semantic similarity scores are mathematically restricted by strict, deterministic entity and safety gates. Generic queries or unverified topics are categorically rejected.
4. **NO VERIFIED MATCH**: When evidence is insufficient, the system safely outputs `NO VERIFIED MATCH` rather than hallucinating an answer.

## Evidence Grounding
Every verified response traces back to a specific, verified knowledge base record. The `EvidencePanel` surfaces the exact official BIS source URL, ensuring users can immediately verify the claim on the actual government portal.

## Multilingual Approach
ManakAI is architecturally built to accept queries in English, Hindi, Marathi, Kannada, Telugu, Tamil, and Gujarati. The LLM normalizes these inputs into English concepts to query the deterministic backend. If the LLM normalization fails, the system safely falls back to native processing or rejects the query, preventing mistranslations from resulting in false compliance advice.

## Scalability & Limitations
The decoupled frontend/backend is infinitely horizontally scalable. However, the current prototype curates a specialized subset of BIS data to demonstrate the concept without running afoul of copyrighted BIS PDFs or scraping protected portals. The core limitation currently is external API rate limits (Gemini HTTP 429), for which the system demonstrates resilient, safe fallback behaviour.

## Why ManakAI is Different
Unlike a generic generative AI chatbot (which might hallucinate a legal requirement) or a simple website search (which requires exact bureaucratic jargon), ManakAI merges the conversational flexibility of AI with the mathematical safety of deterministic databases.
