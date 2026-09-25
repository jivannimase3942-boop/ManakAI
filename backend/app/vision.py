import os
import json
import logging
from typing import Dict, Any, Optional
import tempfile
import io
import math

logger = logging.getLogger(__name__)

# ============================================================
# CONFIGURATION
# ============================================================

HIGH_CONFIDENCE = float(
    os.getenv("VISION_HIGH_CONFIDENCE", "0.75")
)

MEDIUM_CONFIDENCE = float(
    os.getenv("VISION_MEDIUM_CONFIDENCE", "0.50")
)

# Gemini API key
GEMINI_API_KEY = (
    os.getenv("GEMINI_API_KEY", "").strip()
    or os.getenv("GOOGLE_API_KEY", "").strip()
)

# Required model for current ManakAI setup
LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "gemini-3.8-flash"
).strip()


# ============================================================
# WINDOWS TESSERACT CONFIGURATION
# ============================================================

TESSERACT_EXE = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def _configure_tesseract():
    """
    Configure pytesseract to use the installed Windows
    Tesseract executable.

    This prevents:
        TesseractNotFoundError
    when Tesseract is installed but not visible in PATH.
    """

    try:
        import pytesseract

        if os.path.exists(TESSERACT_EXE):
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE

            logger.info(
                "Tesseract configured: %s",
                TESSERACT_EXE
            )

            return pytesseract

        logger.warning(
            "Tesseract executable not found: %s",
            TESSERACT_EXE
        )

        return pytesseract

    except ImportError:
        logger.warning(
            "pytesseract is not installed."
        )
        return None

    except Exception as exc:
        logger.warning(
            "Tesseract configuration failed: %s",
            exc
        )
        return None


# ============================================================
# GEMINI CLIENT
# ============================================================

def _get_genai_client():
    """
    Create a Google GenAI client using the new google-genai SDK.

    IMPORTANT:
    This intentionally does NOT use the deprecated:
        google.generativeai
    """

    if not GEMINI_API_KEY:
        logger.warning(
            "GEMINI_API_KEY / GOOGLE_API_KEY is not configured."
        )
        return None

    try:
        from google import genai

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        return client

    except ImportError:
        logger.error(
            "google-genai is not installed."
        )
        return None

    except Exception as exc:
        logger.error(
            "Failed to create Gemini client: %s",
            exc
        )
        return None


# ============================================================
# FALLBACK RESPONSE
# ============================================================

def _fallback_response(
    err: str = ""
) -> Dict[str, Any]:
    """
    Return a stable response structure so the frontend
    never crashes when Vision/OCR fails.
    """

    response = {
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

        "detected_information": {
            "ocr_text": "",
            "brand": "Not detected",
            "model": "Not detected",
            "bis_information": []
        },

        "identification_status": "failed",

        "confidence_level": "low",

        "multiple_candidates": []
    }

    if err:
        response["error"] = str(err)

    return response


# ============================================================
# CONFIDENCE
# ============================================================

def _confidence_level(
    confidence: float
) -> str:

    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0.0

    if confidence >= HIGH_CONFIDENCE:
        return "high"

    if confidence >= MEDIUM_CONFIDENCE:
        return "medium"

    return "low"


# ============================================================
# SAFE FLOAT
# ============================================================

def _safe_confidence(value: Any) -> float:

    try:
        value = float(value)

        if not math.isfinite(value):
            return 0.0

        return max(
            0.0,
            min(1.0, value)
        )

    except (TypeError, ValueError):
        return 0.0


# ============================================================
# JSON CLEANING
# ============================================================

def _clean_json_text(text: str) -> str:
    """
    Gemini normally returns JSON because response_mime_type
    is application/json.

    This function additionally protects against accidental
    markdown code fences.
    """

    if not text:
        raise ValueError(
            "Gemini returned an empty response."
        )

    text = text.strip()

    # Remove ```json
    if text.startswith("```json"):
        text = text[len("```json"):].strip()

    # Remove ```JSON
    elif text.startswith("```JSON"):
        text = text[len("```JSON"):].strip()

    # Remove generic ```
    elif text.startswith("```"):
        text = text[3:].strip()

    # Remove ending ```
    if text.endswith("```"):
        text = text[:-3].strip()

    return text


# ============================================================
# OCR
# ============================================================

def _extract_ocr(
    file_data: bytes,
    mime_type: str
) -> Dict[str, Any]:

    empty = {
        "ocr_text": "",
        "brand": "Not detected",
        "model": "Not detected",
        "bis_information": []
    }

    # Tesseract OCR is currently intended for images.
    if not mime_type:
        return empty

    if not mime_type.lower().startswith("image/"):
        return empty

    pytesseract = _configure_tesseract()

    if pytesseract is None:
        logger.warning(
            "OCR unavailable: pytesseract could not be loaded."
        )
        return empty

    try:
        from PIL import Image

        image = Image.open(
            io.BytesIO(file_data)
        )

        # Convert to RGB so Tesseract handles image consistently.
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")

        text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        ).strip()

        if not text:
            return empty

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        bis_information = []

        for line in lines:

            lower = line.lower()

            if (
                "bis" in lower
                or "isi" in lower
                or "is " in lower
                or "bureau of indian standards" in lower
            ):
                bis_information.append(line)

        return {
            "ocr_text": text,
            "brand": "Not detected",
            "model": "Not detected",
            "bis_information": bis_information
        }

    except Exception as exc:

        logger.warning(
            "OCR failed: %s",
            exc
        )

        return empty


# ============================================================
# NORMALIZE GEMINI RESULT
# ============================================================

def _normalise_gemini_result(
    result: Dict[str, Any]
) -> Dict[str, Any]:

    if not isinstance(result, dict):
        raise ValueError(
            "Gemini Vision output is not a JSON object."
        )

    # --------------------------------------------------------
    # Support primary schema
    # --------------------------------------------------------

    raw_identification = (
        result.get("product_identification")
        or {}
    )

    if not isinstance(raw_identification, dict):
        raw_identification = {}

    # --------------------------------------------------------
    # Also support flat schema
    # --------------------------------------------------------

    if not raw_identification and result.get(
        "product_name"
    ):

        raw_identification = {
            "name": result.get(
                "product_name"
            ),

            "category": result.get(
                "category"
            ),

            "brand": result.get(
                "brand"
            ),

            "model": result.get(
                "model"
            ),

            "manufacturer": result.get(
                "manufacturer"
            ),

            "confidence": result.get(
                "confidence"
            ),

            "evidence": [
                result.get("reason", "")
            ]
        }

    # --------------------------------------------------------
    # Basic fields
    # --------------------------------------------------------

    name = str(
        raw_identification.get(
            "name",
            result.get(
                "product_name",
                "Not detected"
            )
        )
        or "Not detected"
    ).strip()

    category = str(
        raw_identification.get(
            "category",
            result.get(
                "category",
                "Not detected"
            )
        )
        or "Not detected"
    ).strip()

    brand = str(
        raw_identification.get(
            "brand",
            result.get(
                "brand",
                "Not detected"
            )
        )
        or "Not detected"
    ).strip()

    model = str(
        raw_identification.get(
            "model",
            result.get(
                "model",
                "Not detected"
            )
        )
        or "Not detected"
    ).strip()

    manufacturer = str(
        raw_identification.get(
            "manufacturer",
            result.get(
                "manufacturer",
                "Not detected"
            )
        )
        or "Not detected"
    ).strip()

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    confidence = _safe_confidence(
        raw_identification.get(
            "confidence",
            result.get(
                "confidence",
                0.0
            )
        )
    )

    # --------------------------------------------------------
    # Evidence
    # --------------------------------------------------------

    evidence = raw_identification.get(
        "evidence",
        []
    )

    if not isinstance(evidence, list):
        evidence = []

    cleaned_evidence = []

    for item in evidence:

        value = str(item).strip()

        if value and value not in cleaned_evidence:
            cleaned_evidence.append(value)

    extra_evidence = [
        result.get("visible_text"),
        result.get("visible_markings"),
        result.get("reason")
    ]

    for item in extra_evidence:

        if item:

            value = str(item).strip()

            if (
                value
                and value not in cleaned_evidence
            ):
                cleaned_evidence.append(value)

    # --------------------------------------------------------
    # Not detected protection
    # --------------------------------------------------------

    not_detected = {
        "",
        "not detected",
        "not identified",
        "unknown",
        "none",
        "null",
        "n/a"
    }

    if (
        name.lower() in not_detected
        or category.lower() in not_detected
    ):

        name = "Not detected"
        category = "Not detected"
        confidence = 0.0

        status = "uncertain"

    else:

        # Don't accept high confidence without evidence.
        if (
            confidence >= HIGH_CONFIDENCE
            and not cleaned_evidence
            and brand.lower() in not_detected
            and model.lower() in not_detected
        ):
            confidence = MEDIUM_CONFIDENCE

        status = (
            "identified"
            if confidence >= MEDIUM_CONFIDENCE
            else "uncertain"
        )

    # --------------------------------------------------------
    # Multiple products
    # --------------------------------------------------------

    identification_status = result.get(
        "identification_status"
    )

    if identification_status == "multiple_products":
        status = "multiple_products"

    # --------------------------------------------------------
    # Attributes
    # --------------------------------------------------------

    attributes = result.get(
        "attributes",
        {}
    )

    if not isinstance(attributes, dict):
        attributes = {}

    observed_attributes = result.get(
        "observed_attributes",
        []
    )

    if (
        isinstance(observed_attributes, list)
        and observed_attributes
    ):
        attributes = {
            **attributes,
            "observed": observed_attributes
        }

    # --------------------------------------------------------
    # Multiple candidates
    # --------------------------------------------------------

    multiple_candidates = result.get(
        "multiple_candidates",
        []
    )

    if not isinstance(
        multiple_candidates,
        list
    ):
        multiple_candidates = []

    # --------------------------------------------------------
    # Visible text
    # --------------------------------------------------------

    visible_text = str(
        result.get(
            "visible_text",
            ""
        )
        or ""
    ).strip()

    visible_markings = str(
        result.get(
            "visible_markings",
            ""
        )
        or ""
    ).strip()

    # --------------------------------------------------------
    # Final normalized response
    # --------------------------------------------------------

    return {
        "product_identification": {
            "name": name,
            "category": category,
            "brand": brand,
            "model": model,
            "manufacturer": manufacturer,
            "confidence": round(
                confidence,
                2
            ),
            "evidence": cleaned_evidence
        },

        "attributes": attributes,

        "identification_status": status,

        "confidence_level": _confidence_level(
            confidence
        ),

        "multiple_candidates": multiple_candidates,

        "detected_information": {
            "ocr_text": visible_text,
            "brand": brand,
            "model": model,
            "bis_information": (
                [visible_markings]
                if visible_markings
                else []
            )
        }
    }


# ============================================================
# GEMINI VISION
# ============================================================

def analyze_with_gemini(
    client,
    file_data: bytes,
    mime_type: str,
    query: Optional[str] = None
) -> Dict[str, Any]:

    try:

        # ----------------------------------------------------
        # Strict Vision prompt
        # ----------------------------------------------------

        system_prompt = """
You are ManakAI Vision, a strict product identification
assistant.

Your task is to analyze the supplied image or document.

Identify the product only from observable visual evidence.

Extract:

- product name
- category
- brand
- model
- manufacturer
- visible text
- visible BIS/ISI or other markings
- visible attributes
- confidence
- reason

IMPORTANT RULES:

1. Do NOT hallucinate.
2. Do NOT invent a brand.
3. Do NOT invent a model number.
4. Do NOT invent BIS certification.
5. Do NOT infer certification merely because a product looks
   like a known certified product.
6. If text is unreadable, return an empty string.
7. If a field cannot be identified, return "Not detected".
8. Confidence must represent visual evidence only.
9. User-provided context is only supporting information.
10. User text alone must never increase confidence.
11. If there are multiple products, identify the most prominent
    product and use identification_status =
    "multiple_products".
12. If the product cannot be reliably identified, use
    identification_status = "uncertain".
13. Do not provide web-search claims.
14. Do not claim a product complies with BIS standards unless
    actual visible evidence supports that statement.
15. Keep the reason short and evidence-based.

Return ONLY valid JSON.

Required JSON structure:

{
  "product_identification": {
    "name": "Product Name or Not detected",
    "category": "Broad Category or Not detected",
    "brand": "Brand or Not detected",
    "model": "Model or Not detected",
    "manufacturer": "Manufacturer or Not detected",
    "confidence": 0.0,
    "evidence": []
  },
  "attributes": {
    "voltage": "Not detected",
    "power": "Not detected",
    "capacity": "Not detected",
    "material": "Not detected",
    "intended_use": "Not detected",
    "other": {}
  },
  "identification_status": "identified",
  "multiple_candidates": [],
  "visible_text": "",
  "visible_markings": "",
  "observed_attributes": [],
  "reason": ""
}

Confidence must be between 0.0 and 1.0.
"""

        # ----------------------------------------------------
        # User query
        # ----------------------------------------------------

        user_prompt = (
            "Identify the product in the supplied file."
        )

        if query:
            user_prompt += (
                "\nAdditional user context: "
                + str(query)
            )

        # ----------------------------------------------------
        # Google GenAI image/document part
        # ----------------------------------------------------

        from google.genai import types

        file_part = types.Part.from_bytes(
            data=file_data,
            mime_type=mime_type
        )

        # ----------------------------------------------------
        # Generate content
        # ----------------------------------------------------

        response = client.models.generate_content(
            model=LLM_MODEL,

            contents=[
                system_prompt,
                user_prompt,
                file_part
            ],

            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json"
            )
        )

        # ----------------------------------------------------
        # Read response
        # ----------------------------------------------------

        text = getattr(
            response,
            "text",
            None
        )

        if not text:
            raise ValueError(
                "Gemini returned no text."
            )

        text = _clean_json_text(
            text
        )

        # ----------------------------------------------------
        # Parse JSON
        # ----------------------------------------------------

        try:

            result = json.loads(
                text
            )

        except json.JSONDecodeError as exc:

            logger.error(
                "Gemini returned invalid JSON: %s",
                text[:1000]
            )

            raise ValueError(
                f"Invalid JSON returned by Gemini: {exc}"
            )

        if not isinstance(
            result,
            dict
        ):
            raise ValueError(
                "Gemini output is not a JSON object."
            )

        return _normalise_gemini_result(
            result
        )

    except Exception as exc:

        logger.error(
            "Gemini Vision failed: %s",
            exc
        )

        raise


# ============================================================
# YOLO FALLBACK
# ============================================================

def analyze_with_yolo(
    file_data: bytes
) -> Dict[str, Any]:

    tmp_path = None

    try:

        from ultralytics import YOLO
        from PIL import Image

        # ----------------------------------------------------
        # Load image
        # ----------------------------------------------------

        image = Image.open(
            io.BytesIO(file_data)
        ).convert("RGB")

        # ----------------------------------------------------
        # Temporary file
        # ----------------------------------------------------

        with tempfile.NamedTemporaryFile(
            suffix=".jpg",
            delete=False
        ) as tmp:

            image.save(
                tmp.name,
                format="JPEG"
            )

            tmp_path = tmp.name

        # ----------------------------------------------------
        # Silence Ultralytics logs
        # ----------------------------------------------------

        logging.getLogger(
            "ultralytics"
        ).setLevel(
            logging.WARNING
        )

        # ----------------------------------------------------
        # Load classifier
        # ----------------------------------------------------

        model = YOLO(
            "yolov8n-cls.pt"
        )

        results = model(
            tmp_path,
            verbose=False
        )

        # ----------------------------------------------------
        # Cleanup temp image
        # ----------------------------------------------------

        try:
            os.remove(
                tmp_path
            )
            tmp_path = None
        except Exception:
            pass

        # ----------------------------------------------------
        # Validate result
        # ----------------------------------------------------

        if not results:
            return _fallback_response(
                "YOLO returned no results."
            )

        result = results[0]

        if not hasattr(
            result,
            "probs"
        ) or result.probs is None:

            return _fallback_response(
                "YOLO classification probabilities unavailable."
            )

        names = model.names

        top5_indices = result.probs.top5
        top5_probs = result.probs.top5conf

        if not top5_indices:
            return _fallback_response(
                "YOLO could not classify the image."
            )

        top1_index = top5_indices[0]

        top1_name = str(
            names[top1_index]
        )

        top1_prob = float(
            top5_probs[0].item()
        )

        # ----------------------------------------------------
        # Safe category mapping
        # ----------------------------------------------------

        category_map = {

            "cellular_telephone":
                "Mobile Phone",

            "cellular phone":
                "Mobile Phone",

            "cellphone":
                "Mobile Phone",

            "hand-held_computer":
                "Mobile Phone",

            "laptop":
                "Laptop / Computer",

            "notebook":
                "Laptop / Computer",

            "desktop_computer":
                "Laptop / Computer",

            "water_bottle":
                "Packaged Drinking Water",

            "water_jug":
                "Packaged Drinking Water",

            "crash_helmet":
                "Helmet",

            "helmet":
                "Helmet",

            "computer":
                "Computer",

            "monitor":
                "Monitor",

            "television":
                "Television",

            "television_set":
                "Television",

            "refrigerator":
                "Refrigerator",

            "microwave":
                "Microwave Oven",

            "washing_machine":
                "Washing Machine"
        }

        # ----------------------------------------------------
        # Only trust known mappings
        # ----------------------------------------------------

        if top1_name in category_map:

            detected_name = category_map[
                top1_name
            ]

            confidence = top1_prob

            status = (
                "identified"
                if confidence >= MEDIUM_CONFIDENCE
                else "uncertain"
            )

            evidence = [
                f"Visual classifier detected: {top1_name}"
            ]

        else:

            detected_name = "Not detected"

            confidence = 0.0

            status = "uncertain"

            evidence = []

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return {
            "product_identification": {
                "name": detected_name,
                "category": detected_name,
                "brand": "Not detected",
                "model": "Not detected",
                "manufacturer": "Not detected",
                "confidence": round(
                    confidence,
                    2
                ),
                "evidence": evidence
            },

            "attributes": {},

            "identification_status": status,

            "confidence_level": _confidence_level(
                confidence
            ),

            "multiple_candidates": []
        }

    except Exception as exc:

        logger.error(
            "YOLO Vision error: %s",
            exc
        )

        return _fallback_response(
            str(exc)
        )

    finally:

        if tmp_path:

            try:
                os.remove(
                    tmp_path
                )
            except Exception:
                pass


# ============================================================
# MAIN ANALYSIS FUNCTION
# ============================================================

def analyze_file_content(
    file_data: bytes,
    mime_type: str,
    query: Optional[str] = None
) -> Dict[str, Any]:

    """
    Main ManakAI Vision entry point.

    Flow:

        Image/File
             |
             v
        OCR extraction
             |
             v
        Gemini Vision
             |
       +-----+------+
       |            |
     success      failure
       |            |
       v            v
     result        YOLO
                    |
                    v
                 fallback
    """

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not file_data:

        return _fallback_response(
            "No file data received."
        )

    if not mime_type:

        mime_type = "image/jpeg"

    # --------------------------------------------------------
    # OCR first
    # --------------------------------------------------------

    detected_information = _extract_ocr(
        file_data,
        mime_type
    )

    # --------------------------------------------------------
    # Gemini client
    # --------------------------------------------------------

    client = _get_genai_client()

    gemini_error = None

    # --------------------------------------------------------
    # Gemini Vision
    # --------------------------------------------------------

    if client:

        try:

            logger.info(
                "Running Gemini Vision with model: %s",
                LLM_MODEL
            )

            result = analyze_with_gemini(
                client=client,
                file_data=file_data,
                mime_type=mime_type,
                query=query
            )

            # ------------------------------------------------
            # Merge OCR with Gemini result
            # ------------------------------------------------

            gemini_detected = result.get(
                "detected_information",
                {}
            )

            if not isinstance(
                gemini_detected,
                dict
            ):
                gemini_detected = {}

            merged_information = {
                **detected_information,
                **gemini_detected
            }

            product_info = result.get(
                "product_identification",
                {}
            )

            if not isinstance(
                product_info,
                dict
            ):
                product_info = {}

            # Prefer Gemini brand/model if valid.
            gemini_brand = str(
                product_info.get(
                    "brand",
                    "Not detected"
                )
                or "Not detected"
            )

            gemini_model = str(
                product_info.get(
                    "model",
                    "Not detected"
                )
                or "Not detected"
            )

            if gemini_brand.lower() not in {
                "",
                "not detected",
                "not identified"
            }:
                merged_information["brand"] = (
                    gemini_brand
                )

            if gemini_model.lower() not in {
                "",
                "not detected",
                "not identified"
            }:
                merged_information["model"] = (
                    gemini_model
                )

            result["detected_information"] = (
                merged_information
            )

            # ------------------------------------------------
            # Accept identified or multiple products
            # ------------------------------------------------

            status = result.get(
                "identification_status",
                "uncertain"
            )

            if status in {
                "identified",
                "multiple_products"
            }:

                logger.info(
                    "Gemini Vision successfully identified product."
                )

                return result

            # ------------------------------------------------
            # Gemini uncertain
            # ------------------------------------------------

            gemini_error = (
                "Gemini returned uncertain status."
            )

            logger.warning(
                gemini_error
            )

        except Exception as exc:

            gemini_error = str(
                exc
            )

            logger.error(
                "Gemini Vision failed. Falling back to YOLO: %s",
                exc
            )

    else:

        gemini_error = (
            "Gemini client unavailable or API key not configured."
        )

        logger.warning(
            gemini_error
        )

    # --------------------------------------------------------
    # YOLO fallback
    # --------------------------------------------------------

    try:

        logger.info(
            "Running YOLO fallback."
        )

        yolo_result = analyze_with_yolo(
            file_data
        )

        # ----------------------------------------------------
        # Add Gemini failure information
        # ----------------------------------------------------

        if gemini_error:

            yolo_result["error"] = (
                "Gemini Vision failed or was unavailable. "
                "Fallback used. "
                + gemini_error
            )

        # ----------------------------------------------------
        # Merge OCR information
        # ----------------------------------------------------

        yolo_information = yolo_result.get(
            "detected_information",
            {}
        )

        if not isinstance(
            yolo_information,
            dict
        ):
            yolo_information = {}

        yolo_result["detected_information"] = {
            **detected_information,
            **yolo_information
        }

        return yolo_result

    except Exception as exc:

        logger.error(
            "YOLO fallback failed: %s",
            exc
        )

        error_message = (
            "Both Gemini Vision and YOLO failed. "
            f"Gemini: {gemini_error} | "
            f"YOLO: {exc}"
        )

        fallback = _fallback_response(
            error_message
        )

        fallback[
            "detected_information"
        ] = detected_information

        return fallback


# ============================================================
# OPTIONAL DIRECT IMAGE ANALYSIS ALIAS
# ============================================================

def analyze_image(
    file_data: bytes,
    mime_type: str = "image/jpeg",
    query: Optional[str] = None
) -> Dict[str, Any]:

    """
    Convenience wrapper for image analysis.
    """

    return analyze_file_content(
        file_data=file_data,
        mime_type=mime_type,
        query=query
    )