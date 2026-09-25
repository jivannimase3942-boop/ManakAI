from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import os
import time
import logging
from dotenv import load_dotenv

load_dotenv()

from app.routers import chat, standard_search, services, sources, assistant, analyze
from app import llm

app = FastAPI(
    title="ManakAI API",
    description="Prototype AI assistant for Indian Standards and BIS services Not an official BIS system.",
    version="0.1.0",
)
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:5174,http://localhost:5175,http://localhost:5176,http://127.0.0.1:5173,http://127.0.0.1:5174,http://127.0.0.1:5175,http://127.0.0.1:5176")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Internal server error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please try again."}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Log the specific error server-side, return safe generic to client
    logging.warning(f"Validation error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request input. Please check the provided data."}
    )

# Security and Rate Limiting
RATE_LIMIT_DURATION = 60
RATE_LIMIT_REQUESTS = 30
rate_limits = {}

class SecurityAndRateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Rate Limiting for specific endpoints
        if request.url.path in ["/api/assistant/query", "/api/standard-search"]:
            client_ip = request.client.host if request.client else "127.0.0.1"
            now = time.time()

            if client_ip not in rate_limits:
                rate_limits[client_ip] = {"count": 0, "start_time": now}

            record = rate_limits[client_ip]
            if now - record["start_time"] > RATE_LIMIT_DURATION:
                record["count"] = 1
                record["start_time"] = now
            else:
                record["count"] += 1

            if record["count"] > RATE_LIMIT_REQUESTS:
                # Return standard 429 safely
                return JSONResponse(status_code=429, content={"detail": "Too many requests. Please slow down."})

            # Cleanup memory occasionally
            if len(rate_limits) > 10000:
                stale = [ip for ip, rec in rate_limits.items() if now - rec["start_time"] > RATE_LIMIT_DURATION]
                for ip in stale:
                    del rate_limits[ip]

        # 2. Call next middleware
        response = await call_next(request)

        # 3. Add Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response

app.add_middleware(SecurityAndRateLimitMiddleware)

class UTF8CharsetMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        content_type = response.headers.get("content-type")
        if content_type and "application/json" in content_type and "charset=" not in content_type:
            response.headers["content-type"] = content_type + "; charset=utf-8"
        return response

app.add_middleware(UTF8CharsetMiddleware)

app.include_router(chat.router)
app.include_router(assistant.router)
app.include_router(analyze.router)
app.include_router(standard_search.router)
app.include_router(services.router)
app.include_router(sources.router)
from app.routers import compliance
app.include_router(compliance.router)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "ManakAI backend",
        "llm_configured": llm.is_llm_configured(),
        "mode": "llm" if llm.is_llm_configured() else "demo",
    }



app.include_router(assistant.router)
app.include_router(analyze.router)

