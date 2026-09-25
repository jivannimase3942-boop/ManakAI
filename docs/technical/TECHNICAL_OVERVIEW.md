# ManakAI Technical Overview

## 1. Technology Stack

### Frontend

- React
- Vite
- JavaScript
- Tailwind CSS
- Component-based UI architecture

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- REST API architecture

### AI and Retrieval

- Deterministic intent processing
- Lexical / keyword retrieval
- Semantic embedding retrieval
- Hybrid retrieval
- Optional LLM-based query normalization

### Data

- JSON-based structured knowledge records
- Local embedding cache
- Runtime database files are excluded from the public repository

## 2. Backend Structure

The backend is organized around application modules, API routers, retrieval components, decision logic, and ingestion workflows.

```text
backend/
├── app/
│   ├── decision.py
│   ├── embeddings.py
│   ├── hybrid_retriever.py
│   ├── intent.py
│   ├── knowledge_base.py
│   ├── llm.py
│   ├── models.py
│   ├── rag.py
│   ├── semantic_retriever.py
│   ├── vision.py
│   └── routers/
│
├── scripts/
├── tests/
├── main.py
└── requirements.txt