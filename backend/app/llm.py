"""
Thin wrapper around an API-based LLM. The provider is configurable via
environment variables so the same code path works whether or not an
API key is present. If no key is configured, callers should use the
Demo Mode logic in rag.py instead of calling generate().
"""
import os
from typing import List, Dict

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")

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

