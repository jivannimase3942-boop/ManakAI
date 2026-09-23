from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from ..models import ProductAnalysisResponse, ProductIdentification, ComplianceResponse
from ..vision import analyze_file_content
from .. import decision
import os
import io
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

@router.post("/api/analyze-product", response_model=ProductAnalysisResponse)
async def analyze_product(
    file: UploadFile = File(...),
    language: str = Form("en"),
    query: str = Form(None)
):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    ext = os.path.splitext(file.filename)[1].lower()
    allowed_exts = [".jpg", ".jpeg", ".png", ".webp", ".pdf"]
    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail=f"Unsupported file extension: {ext}")

    # Validate extension & mime
    allowed_types = ["image/jpeg", "image/png", "image/webp", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB.")

    # Magic bytes check
    is_valid_magic = False
    if contents.startswith(b"\xff\xd8\xff"):
        is_valid_magic = True
    elif contents.startswith(b"\x89PNG\r\n\x1a\n"):
        is_valid_magic = True
    elif contents.startswith(b"RIFF") and b"WEBP" in contents[8:12]:
        is_valid_magic = True
    elif contents.startswith(b"%PDF-"):
        is_valid_magic = True

    if not is_valid_magic:
        raise HTTPException(status_code=400, detail="Invalid file format (magic bytes mismatch).")

    source_type = "image"
    if file.content_type == "application/pdf" or ext == ".pdf":
        source_type = "pdf"

    # 1. Vision extraction
    vision_result = analyze_file_content(contents, file.content_type, query)

    status = vision_result.get("identification_status", "failed")
    prod_ident = vision_result.get("product_identification", {})

    # Map to ProductIdentification model
    pi_model = ProductIdentification(
        name=prod_ident.get("name", "Not detected"),
        category=prod_ident.get("category", "Not detected"),
        brand=prod_ident.get("brand", "Not detected"),
        model=prod_ident.get("model", "Not detected"),
        manufacturer=prod_ident.get("manufacturer", "Not detected"),
        confidence=prod_ident.get("confidence", 0.0),
        evidence=prod_ident.get("evidence", []),
        status=status
    )

    base_response = {
        "success": True,
        "source_type": source_type,
        "product_identification": pi_model,
        "attributes": vision_result.get("attributes", {}),
        "multiple_candidates": vision_result.get("multiple_candidates", []),
        "error": vision_result.get("error")
    }

    if status in ["failed", "uncertain", "multiple_products"]:
        return ProductAnalysisResponse(**base_response)

    # 2. BIS Mapping using existing decision engine
    # Create an augmented query describing the identified product
    search_query = f"{pi_model.name} {pi_model.category}"
    if pi_model.brand and pi_model.brand.lower() != "not detected":
        search_query += f" {pi_model.brand}"
    if query:
        search_query += f" {query}"

    try:
        compliance_res = decision.generate_compliance_response(search_query, "consumer", language)

        # Merge compliance result into final response
        res_dict = base_response.copy()
        comp_dict = compliance_res.dict()
        for k, v in comp_dict.items():
            res_dict[k] = v

        return ProductAnalysisResponse(**res_dict)
    except Exception as e:
        logger.error(f"Error in decision engine: {e}")
        base_response["error"] = str(e)
        return ProductAnalysisResponse(**base_response)
