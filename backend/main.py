from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routers import chat, standard_search, services, sources, assistant
from app import llm

load_dotenv()

app = FastAPI(
    title="ManakAI API",
    description="Prototype AI assistant for Indian Standards and BIS services (SIH 2026 — SIH26107). Not an official BIS system.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(assistant.router)
app.include_router(standard_search.router)
app.include_router(services.router)
app.include_router(sources.router)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "ManakAI backend",
        "llm_configured": llm.is_llm_configured(),
        "mode": "llm" if llm.is_llm_configured() else "demo",
    }
