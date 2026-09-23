# ManakAI Demo Architecture

## 1. System Topology for SIH Demo
ManakAI operates using a decoupled frontend/backend architecture designed for lightweight, rapid demonstrations.

- **Frontend Environment**: React + Vite SPA (Deployed on Vercel or running locally).
- **Backend Environment**: Python FastAPI (Deployed on Render or running locally).
- **Knowledge Base**: Curated, file-based (`knowledge_base.json`) subset of verified BIS data for zero-latency demonstration.
- **LLM Integration**: Gemini API utilized exclusively via `llm.py` for query normalization.

## 2. Supported Multilingual Architecture
ManakAI is architecturally capable of processing queries in:
- English
- Hindi
- Marathi
- Kannada
- Telugu
- Tamil
- Gujarati

*Note: Multilingual processing is architecturally supported and undergoing live validation. 100% real-world multilingual accuracy is currently limited externally by Gemini API throughput constraints (HTTP 429 errors), which trigger the system's safe deterministic fallback.*

## 3. Scale and Persistence
For the scope of the national-level demonstration, ManakAI relies on local state (browser logic) and a verified JSON dataset.
It intentionally omits complex RDBMS (e.g., PostgreSQL) or Vector Database (e.g., MongoDB/FAISS) infrastructure to prioritize retrieval transparency, security auditing, and rapid iterative UI testing.
