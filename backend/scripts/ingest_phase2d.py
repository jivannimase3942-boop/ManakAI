import json
import os
import sys

from datetime import datetime
from pydantic import ValidationError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ingestion.schemas import IngestionRecord, VerificationStatus
from app.ingestion.validator import validate_and_store

DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/knowledge_base.json"))

def load_kb():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_kb(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

def main():
    existing_records = load_kb()

    # Track existing IS numbers to prevent duplicates
    existing_is_numbers = [r.get("standard_number") for r in existing_records if r.get("standard_number")]

    new_candidates = [
        {
            "id": "kb-010",
            "title": "Safety of Toys: Part 1 Safety Aspects Related to Mechanical and Physical Properties",
            "product_domain": "Toys (Non-Electric)",
            "service_category": "Product Certification (Scheme-I)",
            "standard_number": "IS 9873",
            "standard_title": "Safety of Toys: Part 1 Safety Aspects Related to Mechanical and Physical Properties",
            "topic": "Toys",
            "summary": "Mandatory for all non-electric toys intended for use in play by children under 14 years.",
            "applicability": "Mandatory for all non-electric toys intended for use in play by children under 14 years.",
            "requirements": ["Mechanical and physical safety properties as per the standard."],
            "testing_information": {
                "available": True,
                "details": ["Testing must be conducted at a BIS-empanelled NABL-accredited laboratory."]
            },
            "certification_information": {
                "available": True,
                "scheme": "Scheme-I (ISI Mark) - Toys (Quality Control) Order, 2020",
                "steps": [
                    "Domestic manufacturers apply via Manakonline",
                    "Foreign manufacturers apply via FMCD",
                    "Follow 10 steps to BIS Licence for Toys"
                ]
            },
            "consumer_actions": [
                "Check for the ISI Mark on the toy packaging.",
                "Ensure the toy is age-appropriate."
            ],
            "industry_actions": [
                "Download the official Product Manual for IS 9873.",
                "Ensure samples are tested at an empanelled lab.",
                "Apply for a licence via Manakonline (for domestic manufacturers)."
            ],
            "documents": [],
            "source_name": "BIS Compulsory Certification",
            "source_url": "https://www.bis.gov.in/product-certification/products-under-compulsory-certification/",
            "source_type": "official",
            "verification_status": "VERIFIED",
            "source_checked_date": "2026-09-08",
            "notes_evidence": "Governed by DPIIT QCO 2020. Safe and verified."
        },
        {
            "id": "kb-011",
            "title": "Ordinary Portland Cement - Specification",
            "product_domain": "Ordinary Portland Cement (OPC)",
            "service_category": "Product Certification (Scheme-I)",
            "standard_number": "IS 269",
            "standard_title": "Ordinary Portland Cement - Specification",
            "topic": "Cement",
            "summary": "Mandatory for OPC manufactured or sold in India.",
            "applicability": "Mandatory for OPC manufactured or sold in India.",
            "requirements": ["Chemical and physical requirements (compressive strength, setting time)."],
            "testing_information": {
                "available": True,
                "details": ["Refer to Product Manual PM/IS 269 for sampling and testing guidelines."]
            },
            "certification_information": {
                "available": True,
                "scheme": "Scheme-I (ISI Mark) - Cement (Quality Control) Order, 2003",
                "steps": ["Apply via BIS portal", "factory audit", "grant of licence"]
            },
            "consumer_actions": [
                "Verify the ISI mark on the cement bag.",
                "Check the manufacturing date."
            ],
            "industry_actions": [
                "Ensure manufacturing process meets IS 269.",
                "Establish required in-house testing equipment as per PM/IS 269."
            ],
            "documents": [],
            "source_name": "BIS Compulsory Certification",
            "source_url": "https://www.bis.gov.in/product-certification/products-under-compulsory-certification/",
            "source_type": "official",
            "verification_status": "VERIFIED",
            "source_checked_date": "2026-09-08",
            "notes_evidence": "Cement QCO 2003 is strictly enforced."
        },
        {
            "id": "kb-012",
            "title": "Information Technology Equipment - Safety - General Requirements",
            "product_domain": "Laptops / Notebooks / Tablets",
            "service_category": "Compulsory Registration Scheme (CRS)",
            "standard_number": "IS 13252",
            "standard_title": "Information Technology Equipment - Safety - General Requirements",
            "topic": "Electronics / IT Goods",
            "summary": "Mandatory for all laptops, notebooks, and tablets manufactured, imported, or sold in India.",
            "applicability": "Mandatory for all laptops, notebooks, and tablets manufactured, imported, or sold in India.",
            "requirements": ["Safety requirements for IT equipment."],
            "testing_information": {
                "available": True,
                "details": ["Product must be tested at a BIS-recognized laboratory."]
            },
            "certification_information": {
                "available": True,
                "scheme": "Scheme-II (Self-Declaration of Conformity)",
                "steps": [
                    "Test product at recognized lab",
                    "register online on CRS portal",
                    "generate registration number",
                    "apply Standard Mark"
                ]
            },
            "consumer_actions": [
                "Check for the BIS Standard Mark and Registration Number (R-XXXXXXXX) on the device or packaging.",
                "Verify the registration via the BIS Care App."
            ],
            "industry_actions": [
                "Get the product tested at a BIS-recognized lab.",
                "Register under the CRS scheme online.",
                "Foreign manufacturers must appoint an Authorized Indian Representative (AIR)."
            ],
            "documents": [],
            "source_name": "BIS CRS Scheme",
            "source_url": "https://www.bis.gov.in/registration-scheme/",
            "source_type": "official",
            "verification_status": "VERIFIED",
            "source_checked_date": "2026-09-08",
            "notes_evidence": "MeitY notified product under CRS."
        },
        {
            "id": "kb-013",
            "title": "Protective Helmets for Two Wheeler Riders - Specification",
            "product_domain": "Protective Helmets for Two-Wheeler Riders",
            "service_category": "Product Certification (Scheme-I)",
            "standard_number": "IS 4151",
            "standard_title": "Protective Helmets for Two Wheeler Riders - Specification",
            "topic": "Safety Equipment",
            "summary": "Mandatory for all protective helmets for two-wheeler riders.",
            "applicability": "Mandatory for all protective helmets for two-wheeler riders.",
            "requirements": ["Impact absorption, penetration resistance, rigidity, and retention system testing."],
            "testing_information": {
                "available": True,
                "details": ["Refer to Product Manual for IS 4151."]
            },
            "certification_information": {
                "available": True,
                "scheme": "Scheme-I (ISI Mark)",
                "steps": ["Application", "factory audit", "testing", "grant of licence"]
            },
            "consumer_actions": [
                "Always buy a helmet with a genuine ISI mark.",
                "Verify the manufacturer's licence number via the BIS Care App."
            ],
            "industry_actions": [
                "Ensure the helmet conforms to IS 4151 safety specifications.",
                "Apply for a BIS licence to manufacture or sell."
            ],
            "documents": [],
            "source_name": "BIS Compulsory Certification",
            "source_url": "https://www.bis.gov.in/product-certification/products-under-compulsory-certification/",
            "source_type": "official",
            "verification_status": "VERIFIED",
            "source_checked_date": "2026-09-08",
            "notes_evidence": "Subject to strict QCOs. Sale of non-ISI helmets is illegal."
        },
        {
            "id": "kb-014",
            "title": "Domestic Pressure Cookers - Specification",
            "product_domain": "Domestic Pressure Cookers",
            "service_category": "Product Certification (Scheme-I)",
            "standard_number": "IS 2347",
            "standard_title": "Domestic Pressure Cookers - Specification",
            "topic": "Household Appliances",
            "summary": "Mandatory for all domestic pressure cookers manufactured or sold in India.",
            "applicability": "Mandatory for all domestic pressure cookers manufactured or sold in India.",
            "requirements": ["Safety and performance specifications (operating pressure, bursting pressure, material requirements)."],
            "testing_information": {
                "available": True,
                "details": ["Testing covers pressure relief valve functionality and bursting strength."]
            },
            "certification_information": {
                "available": True,
                "scheme": "Scheme-I (ISI Mark)",
                "steps": ["Application", "factory audit", "testing", "grant of licence"]
            },
            "consumer_actions": [
                "Verify the ISI mark on the pressure cooker before purchase.",
                "Ensure the safety valve is intact."
            ],
            "industry_actions": [
                "Comply with IS 2347 specifications.",
                "Ensure rubber gaskets used also comply with IS 7466."
            ],
            "documents": [],
            "source_name": "BIS Compulsory Certification",
            "source_url": "https://www.bis.gov.in/product-certification/products-under-compulsory-certification/",
            "source_type": "official",
            "verification_status": "VERIFIED",
            "source_checked_date": "2026-09-08",
            "notes_evidence": "Frequent CCPA enforcement against non-compliant cookers on e-commerce."
        }
    ]

    added = 0
    skipped = []

    for candidate in new_candidates:
        # Validate through Pydantic
        try:
            record_obj = IngestionRecord(**candidate)
            validated_dict = record_obj.model_dump()
            # Convert datetime to string for json serialization
            validated_dict["collected_at"] = validated_dict["collected_at"].isoformat()
            if validated_dict["last_verified"]:
                validated_dict["last_verified"] = validated_dict["last_verified"].isoformat()
            validated_dict["verification_status"] = validated_dict["verification_status"].value
            # In knowledge_base.json we map testing_information to testing, certification_information to certification
            # to remain strictly compatible with existing JSON structure.
            validated_dict["testing"] = validated_dict.pop("testing_information")
            validated_dict["certification"] = validated_dict.pop("certification_information")

            # Check duplicate IS number or duplicate ID
            if validated_dict.get("standard_number") in existing_is_numbers:
                skipped.append(f"{candidate['id']} - Duplicate standard number {validated_dict.get('standard_number')}")
                continue
            if any(r["id"] == candidate["id"] for r in existing_records):
                skipped.append(f"{candidate['id']} - Duplicate ID")
                continue

            existing_records.append(validated_dict)
            existing_is_numbers.append(validated_dict.get("standard_number"))
            added += 1
        except ValidationError as e:
            skipped.append(f"{candidate['id']} - Validation failed: {e}")

    # Also record kb-009 as skipped explicitly for logging
    skipped.append("kb-009 - Skipped intentionally to prevent duplicate IS 14543 record (already exists as kb-001).")

    if added > 0:
        save_kb(existing_records)

    print(f"Added: {added}")
    print("Skipped:")
    for s in skipped:
        print(s)

if __name__ == "__main__":
    main()
