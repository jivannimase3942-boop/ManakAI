import os
import json
import logging
from typing import Dict, Any, Optional
import tempfile
import io

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

def _fallback_response(err: str) -> Dict[str, Any]:
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
        "error": err
    }

def analyze_with_yolo(file_data: bytes) -> Dict[str, Any]:
    try:
        from ultralytics import YOLO
        from PIL import Image
        
        img = Image.open(io.BytesIO(file_data)).convert('RGB')
        
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            img.save(tmp.name)
            tmp_path = tmp.name
        
        # Disable ultralytics logging so it doesn't clutter
        import logging
        logging.getLogger("ultralytics").setLevel(logging.WARNING)
        
        model = YOLO('yolov8n-cls.pt')
        results = model(tmp_path, verbose=False)
        os.remove(tmp_path)
        
        names = model.names
        top5_indices = results[0].probs.top5
        top5_probs = results[0].probs.top5conf
        
        category_map = {
            'cellular_telephone': 'Mobile Phone',
            'cellular phone': 'Mobile Phone',
            'cellphone': 'Mobile Phone',
            'hand-held_computer': 'Mobile Phone',
            'laptop': 'Laptop / Computer',
            'notebook': 'Laptop / Computer',
            'desktop_computer': 'Laptop / Computer',
            'water_bottle': 'Packaged Drinking Water',
            'water_jug': 'Packaged Drinking Water',
            'crash_helmet': 'Helmet'
        }
        
        top1_name = names[top5_indices[0]]
        top1_prob = top5_probs[0].item()
        
        if top1_name in category_map and top1_prob > 0.02:
            detected_name = category_map[top1_name]
            confidence = top1_prob
        else:
            detected_name = top1_name.replace('_', ' ').title()
            confidence = top1_prob
            
        status = "identified" if confidence >= 0.1 else "uncertain"
            
        return {
            "product_identification": {
                "name": detected_name,
                "category": detected_name,
                "brand": "Not identified",
                "model": "Not identified",
                "manufacturer": "Not identified",
                "confidence": round(confidence, 2),
                "evidence": [f"Visual AI detected {names[top5_indices[0]]}"]
            },
            "attributes": {},
            "identification_status": status,
            "multiple_candidates": []
        }
    except Exception as e:
        logger.error(f"YOLO Vision error: {e}")
        return _fallback_response(str(e))

def analyze_with_gemini(genai, file_data: bytes, mime_type: str, query: Optional[str] = None):
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
    
    prod_id = result.get("product_identification", {})
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

def analyze_file_content(file_data: bytes, mime_type: str, query: Optional[str] = None) -> Dict[str, Any]:
    genai = _get_genai()
    gemini_error = None
    
    if genai:
        try:
            res = analyze_with_gemini(genai, file_data, mime_type, query)
            # If Gemini confidently identifies something or returns multiple products, use it
            if res.get("identification_status") in ["identified", "multiple_products"]:
                return res
            # If Gemini explicitly returns uncertain/failed gracefully, we can also fall back
            gemini_error = "Gemini returned uncertain/failed status."
        except Exception as e:
            logger.error(f"Gemini API error, falling back to YOLO: {e}")
            gemini_error = str(e)
            
    # Fallback to YOLO if Gemini failed or wasn't available
    try:
        yolo_res = analyze_with_yolo(file_data)
        if gemini_error:
            yolo_res["error"] = f"Gemini fallback triggered: {gemini_error}"
        return yolo_res
    except Exception as e:
        logger.error(f"YOLO fallback error: {e}")
        err_msg = f"Both Gemini and YOLO failed. Gemini: {gemini_error} | YOLO: {e}" if gemini_error else str(e)
        return _fallback_response(err_msg)
