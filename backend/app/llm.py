"""
Thin wrapper around an API-based LLM. The provider is configurable via
environment variables so the same code path works whether or not an
API key is present. If no key is configured, callers should use the
Demo Mode logic in rag.py instead of calling generate().
"""
import os
from typing import List, Dict, Any

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-3.5-flash")

_configured = False

if GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        _configured = True
    except ImportError:
        pass

def is_llm_configured() -> bool:
    return _configured

def generate(system_prompt: str, user_prompt: str) -> str:
    if not is_llm_configured():
        raise RuntimeError("No LLM API key configured")

    import google.generativeai as genai
    model = genai.GenerativeModel(
        model_name=LLM_MODEL,
        system_instruction=system_prompt
    )
    response = model.generate_content(user_prompt)
    return response.text.strip()

def extract_query_context(query: str) -> Dict[str, Any]:
    """
    Extracts normalization context from the query using the LLM.
    Returns a dictionary with:
    - normalized_query: English translation of the query
    - product_entity: Specific product/good/domain mentioned (or empty/null)
    - service_entity: Specific service action mentioned (or empty/null)
    - confidence: 0.0 to 1.0
    - reason: Brief reasoning for the extraction
    """
    if not is_llm_configured():
        return {}

    system_prompt = """You are a BIS (Bureau of Indian Standards) query analyzer.
Your ONLY job is to normalize the user's query and extract entities into structured JSON.
CRITICAL RULES:
1. Normalize only. Do NOT answer the BIS question.
2. Do NOT invent standard numbers, identifiers, or certification requirements.
3. Preserve uncertainty. Return low confidence (< 0.5) when ambiguous.
4. Return no normalization (empty strings and low confidence) when the query is purely unrelated or unknown (e.g. aircraft certification, flying cars).
5. Generic queries (e.g., "testing", "certification", "BIS standard") must NOT trigger normalization into a random product. Set product_entity to "" and return high confidence for the service_entity if applicable.

Return valid JSON exactly matching this format:
{
  "normalized_query": "string (English translation of the query)",
  "product_entity": "string (specific product/good/domain, or empty string if none)",
  "service_entity": "string (specific service/action like 'certification', 'testing', or empty string)",
  "confidence": float (0.0 to 1.0),
  "reason": "string"
}"""

    try:
        import google.generativeai as genai
        import json
        model = genai.GenerativeModel(
            model_name=LLM_MODEL,
            system_instruction=system_prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        response = model.generate_content(query)
        data = json.loads(response.text)

        # Ensure confidence is present
        if "confidence" not in data:
            data["confidence"] = 1.0

        return data
    except Exception as e:
        print(f"LLM Extraction failed: {e}")
        return {}

