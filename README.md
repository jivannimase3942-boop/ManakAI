# ManakAI - BIS Standards Decision and Action Assistant

**Smart India Hackathon 2026 — Problem Statement SIH26107**

> ⚠️ **PROTOTYPE DISCLAIMER**
> This is a hackathon prototype demonstration for SIH 2026. It is **not** an official Bureau of Indian Standards (BIS) service, and it is not affiliated with or endorsed by BIS. Do not rely on this system for legal or compliance decisions. Please verify all requirements with official BIS sources (bis.gov.in).

## Project Overview

ManakAI is an AI-powered BIS Standards Decision and Action Assistant designed for industries, MSMEs, and consumers.

### Why this is different from Google
Google helps users *find* information (returning links and documents). ManakAI helps users *understand what applies* and *decide what to do next*.

### Why this is different from generic chatbots
Generic AI (like ChatGPT) helps users *generate answers*, which often leads to hallucinated standards, clauses, or non-existent laboratory names. ManakAI uses a deterministic rule engine to map intents to a **verified knowledge base**, structuring the response into actionable compliance steps rather than writing long, unstructured paragraphs.

## Architecture

ManakAI operates using a deterministic Decision Engine supported by an optional LLM layer for conversational polishing.

```text
USER QUERY
    │
    ▼
DETERMINISTIC INTENT CLASSIFICATION (Rule-based)
    │
    ▼
RAG / RETRIEVAL ENGINE (Keyword/Phrase overlap)
    │
    ▼
MATCHED VERIFIED KNOWLEDGE RECORD (JSON)
    │
    ▼
DECISION ENGINE (Maps data to a structured Compliance Response)
    │
    ▼
OPTIONAL LLM LAYER (Polishes 'Why this applies' text only)
    │
    ▼
STRUCTURED DASHBOARD UI (Industry / Consumer Modes)
```

### Knowledge Base
The knowledge base (`data/knowledge_base.json`) uses a structured compliance data model. Every fact is mapped to a specific property (requirements, testing, certification, required documents, etc.). If information is missing, the system explicitly states that it is unavailable rather than fabricating an answer.

### Retrieval Engine
The search mechanism parses the user query and uses token overlap and exact phrase matching against titles, standard numbers, and keywords to rank relevant records. It assigns confidence scores (High, Medium, Low, None) to prevent unrelated matches.

### Decision Engine
The core of ManakAI is the `decision.py` module. It consumes the user query, detects the intent, retrieves the best-matching record, and enforces the structured `ComplianceResponse`. This ensures the output is always actionable and evidence-backed.

## API Endpoints

- `GET /api/health` - Check backend health and LLM status.
- `POST /api/assistant/query` - Submit a natural language query. Returns a structured `ComplianceResponse`.
- `POST /api/standard-search` - Search specifically for a standard. Returns a `ComplianceResponse`.
- `GET /api/services` - List available BIS services (Demo).
- `GET /api/sources` - List of verified sources (Demo).

## Local Setup

### Prerequisites
- Node.js 18+
- Python 3.10+

### Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
The API will run at `http://localhost:8000`.

### Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```
The app will run at `http://localhost:5173`.

### Environment Variables
Copy `.env.example` to `backend/.env` (optional):
```bash
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MODEL=gemini-1.5-flash
```
**Note:** The system is designed to work completely offline and deterministically. If `GEMINI_API_KEY` is not provided, the application runs entirely on the internal Decision Engine without any degradation in structured compliance facts.

## Demo Questions

1. `bis standard for drinking water`
2. `I manufacture packaged drinking water. What do I need?`
3. `how can I apply for BIS certification?`
4. `where can I test my product?`
5. `what is hallmarking?`
6. `which BIS scheme applies to electronics?`
7. `how can a consumer verify HUID?`

## Limitations
- This prototype uses a local JSON file (`data/knowledge_base.json`) containing only 8 curated demo records.
- The retrieval engine is a lightweight token-overlap implementation to ensure ease of deployment during the hackathon.
- There are no live integrations with the official BIS Care API or CMS/e-BIS portals.

## Future Scope
- **Vector Database:** Replace the JSON store with a vector database (like FAISS, Chroma, or pgvector) and embeddings for true semantic search.
- **Document Ingestion:** Implement OCR and PDF parsing to automatically update the knowledge base from official BIS gazette notifications.
- **Live Verification:** Integrate with official BIS APIs for real-time licence, HUID, and laboratory status verification.
