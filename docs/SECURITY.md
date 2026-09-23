# ManakAI Security Architecture

## Threat Model & Trust Boundaries
- **Untrusted User Input:** All queries, history objects, and API requests from the frontend or direct API calls are strictly untrusted and undergo Pydantic schema validation.
- **Trusted Knowledge Base:** The backend relies on a strictly curated local data/knowledge_base.json. The RAG/composer pipeline grounds all answers explicitly in this local data. We do NOT allow LLM hallucination for factual answers.
- **Frontend-Backend Boundary:** The React frontend runs purely client-side. The backend exposes explicit endpoints ["/api/assistant/query", "/api/standard-search"] which manage context resolution safely. No secret API keys (LLM/DB) are exposed to the frontend.

## Secret Handling
- Secrets (GEMINI_API_KEY, etc.) reside safely in environment variables.
- .env files are ignored via .gitignore.
- Global error handlers guarantee exceptions do not leak stack traces or environment variables to the frontend.
- API keys are never bundled in frontend production builds (dist/).

## CORS Policy
- Allowed origins are explicitly restricted in production via the ALLOWED_ORIGINS environment variable.
- In local development, defaults restrict to http://localhost:5173, 5174, 5175.
- Wildcard * origins have been explicitly removed to prevent cross-origin exploitation.

## Input & Rate Limiting
- **Rate Limit:** 30 requests per minute per IP via an in-memory sliding token bucket on expensive endpoints. Excess requests receive HTTP 429.
- **Request Size:** Queries and history items are strictly bounded to 500 characters. Message history length is bounded to a maximum of 15 elements to prevent excessive context size.
- Validation rejections yield safe HTTP 422 standard JSON responses without tracebacks.

## Error Handling
- Safe, generic 500 error responses are returned for unhandled internal exceptions ("An internal error occurred. Please try again.").
- Detailed exception data is logged strictly server-side using the Python logging module.

## Security Headers
The API explicitly injects:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- Referrer-Policy: strict-origin-when-cross-origin

## Frontend Security (XSS / URL)
- React inherently prevents most XSS by treating strings as text natively.
- No dangerouslySetInnerHTML, eval, or Function() constructor patterns were found rendering user content.
- External URLs provided by the trusted KB use strict secure protocols (HTTPS).

## Voice Security
- The Voice UI sends finalized transcripts matching the exact API definitions of typed interactions.
- Audio transcriptions undergo the identical strict query length (500 chars max) and rate-limit constraints as standard text.

## Known Limitations
- The current Rate Limiter is a lightweight, bounded in-process dictionary designed for single-instance demo usage. It does not synchronize state across multiple server instances (e.g., workers or horizontal scaling) and relies on rudimentary in-memory eviction. For a full production deployment, a distributed backend like Redis + standard API Gateway layer is recommended.
- A Content Security Policy (CSP) was deferred from backend HTTP header injection to avoid breaking the Vite/React local dev server pipeline (which relies heavily on inline eval and styles). In a strict production environment, this should be enforced at the frontend CDN/Nginx layer.
