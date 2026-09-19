import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-3.5-flash") # or a vision model if necessary

def _get_genai():
    if not GEMINI_API_KEY or GEMINI_API_KEY == "FAKE":
        return None
    try:
        import google.generativeai as genai
        return genai
    except ImportError:
        return None

def analyze_file_content(file_data: bytes, mime_type: str, query: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyzes an image or PDF file using Gemini Vision capabilities.
    Returns a structured dictionary mapping to the Product Identification schema.
    """
    try:
        genai = _get_genai()
        if not genai:
            raise RuntimeError("Vision API is not configured or unavailable.")

        model = genai.GenerativeModel(model_name=LLM_MODEL)

        system_prompt = """
        You are ManakAI Vision, a strict product identification assistant.
        Analyze the provided image or document to identify the product.
        Extract the product name, category, brand, model, manufacturer, and any visible attributes (voltage, power, capacity, material, intended use).
        Do NOT hallucinate. If a value is not visible or identifiable, use "Not detected".
        If the image contains multiple distinct products, identify the most prominent ones and set identification_status to "multiple_products".
        IMPORTANT: If the user provides additional context (e.g., selecting a specific product), you MUST focus only on that specific product and set identification_status to "identified".
        If you cannot identify the product at all, set identification_status to "uncertain" and confidence to a low value.

        Return the response ONLY as a raw JSON object with the following schema:
        {
          "product_identification": {
            "name": "Product Name",
            "category": "Broad Category",
            "brand": "Brand Name or Not detected",
            "model": "Model or Not detected",
            "manufacturer": "Manufacturer or Not detected",
            "confidence": 0.95,
            "evidence": ["Text from image", "Visible features"]
          },
          "attributes": {
            "voltage": "...",
            "power": "...",
            "capacity": "...",
            "material": "...",
            "intended_use": "...",
            "other": {}
          },
          "identification_status": "identified|partially_identified|uncertain|failed|multiple_products",
          "multiple_candidates": [
             { "name": "...", "category": "..." }
          ]
        }

        Only output the JSON object, no markdown, no backticks.
        """

        user_prompt = "Identify the product in this file."
        if query:
            user_prompt += f" User additional context: {query}"

        part = {
            "mime_type": mime_type,
            "data": file_data
        }

        response = model.generate_content([system_prompt, user_prompt, part])
        text = response.text.strip()

        if text.startswith("`json"):
            text = text[7:]
        if text.startswith("`"):
            text = text[3:]
        if text.endswith("`"):
            text = text[:-3]

        result = json.loads(text.strip())

        if not isinstance(result, dict):
            raise ValueError("Vision output is not a JSON object")

        prod_id = result.get("product_identification", {})
        if not isinstance(prod_id, dict):
            prod_id = {}

        return {
            "product_identification": {
                "name": str(prod_id.get("name", "Not detected")),
                "category": str(prod_id.get("category", "Not detected")),
                "brand": str(prod_id.get("brand", "Not detected")),
                "model": str(prod_id.get("model", "Not detected")),
                "manufacturer": str(prod_id.get("manufacturer", "Not detected")),
                "confidence": float(prod_id.get("confidence", 0.0)),
                "evidence": prod_id.get("evidence", []) if isinstance(prod_id.get("evidence"), list) else []
            },
            "attributes": result.get("attributes", {}) if isinstance(result.get("attributes"), dict) else {},
            "identification_status": str(result.get("identification_status", "identified")),
            "multiple_candidates": result.get("multiple_candidates", []) if isinstance(result.get("multiple_candidates"), list) else []
        }
    except Exception as e:
        logger.error(f"Vision API error: {e}")
        return {
            "product_identification": {
                "name": "Not detected",
                "category": "Not detected",
                "brand": "Not detected",
                "model": "Not detected",
                "manufacturer": "Not detected",
                "confidence": 0.0,
                "evidence": []
            },
            "attributes": {},
            "identification_status": "failed",
            "error": str(e)
        }
