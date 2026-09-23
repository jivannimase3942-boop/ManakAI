# Phase 2F Implementation Plan
**End-To-End Knowledge + Backend + UI Implementation**

## 1. Current System Inspection
* **Response Schema**: Defined in `backend/app/models.py` (`ComplianceResponse`). Mostly uses flat lists (`List[str]`) for `requirements`, `required_documents`, `testing`, `certification_steps`, `next_actions`, etc.
* **KB Schema**: Defined in `data/knowledge_base.json`. Records contain string fields or localized lists under `i18n` (e.g., `requirements`, `testing.details`, `certification.steps`). No structured representation of explicit documents, fees, or compliance steps with missing states.
* **Frontend Rendering**: Handled in `DecisionCard.jsx` and `ComplianceJourney.jsx`. Relies on mapping simple string lists to hardcoded UI cards (`jProduct`, `jStandard`, `jPathway`, `jTesting`, `jDocs`, `jNext`). Source links exist globally for the standard (`sources: List[SourceRef]`), but not per-step/per-requirement.

## 2. Proposed Schema Changes (Backward Compatible)
We will extend the schemas to support rich objects without breaking legacy string-based parsing.

**Knowledge Base Schema (Optional Fields)**
```json
{
  "product_domain": "...",
  "product_name": "...",
  "service_category": "...",
  "standard": { "number": "...", "title": "...", "status": "...", "valid_from": "...", "valid_until": "..." },
  "regulatory_status": { "status": "...", "regulation": "...", "notification": "...", "ministry": "...", "effective_date": "..." },
  "scheme": { "name": "...", "type": "...", "validity": "..." },
  "applicant": { "eligible": [], "requirements": [] },
  "requirements": [], // Structured list
  "testing": { "required": true, "standard": "...", "laboratory": "...", "lab_finder": {} },
  "documents": [], // Structured list
  "fees": {},
  "application_process": [],
  "marking": {},
  "post_registration": [],
  "consumer_actions": [],
  "industry_actions": [],
  "compliance_journey": [
    {
      "step": 1,
      "title": "Prepare Applicant Documents",
      "description": "...",
      "requirements": [
        {
          "id": "pan",
          "name": "PAN Card",
          "required": true,
          "status": "MISSING",
          "if_missing": { "message": "...", "action": { "label": "Get PAN Card", "url": "OFFICIAL_URL", "type": "official_service" } }
        }
      ]
    }
  ],
  "official_links": [
    { "title": "...", "type": "...", "url": "...", "description": "...", "checked_date": "..." }
  ],
  "evidence": [],
  "source_checked_date": "...",
  "notes_evidence": "..."
}
```

**Backend API (`ComplianceResponse`) changes**
We will add `Optional[List[Dict[str, Any]]]` fields for `structured_compliance_journey`, `structured_testing`, `structured_documents`, `structured_fees`, `structured_evidence`, `official_links`, and `regulatory_status`.
This ensures existing frontends expecting `testing: List[str]` will not crash, while updated components can conditionally render the `structured_*` keys if present.

## 3. Backend Implementation Strategy
1. **Model Updates**: Extend `ComplianceResponse` in `backend/app/models.py`.
2. **Decision Engine (`decision.py`)**: Update `generate_standard_response` to extract the new structured fields from the `record` if they exist, and map them to the response output.
3. **Intent / Fallbacks**: Maintain absolute preservation of intent matching, exact ID lookup, and adversarial filtering. If a structured requirement cannot be verified, it will be marked as `UNAVAILABLE` or omitted.

## 4. Frontend UI Strategy
1. **DecisionCard / ComplianceJourney Updates**: Refactor UI to detect if `structured_compliance_journey` exists. If so, render a beautiful step-by-step timeline (e.g. `STEP 1 Prepare Documents`).
2. **Missing Prerequisite UI**: Add conditional rendering inside the timeline steps to explicitly surface missing prerequisites (e.g. `PAN Card ❌`) and render official action buttons `[Get PAN Card →]` using the provided verified URL (`target="_blank" rel="noopener noreferrer"`).
3. **Structured Evidence Cards**: Replace flat lists with distinct sections (Regulatory Status, Fees, Evidence, Documents) mapped to the new structured data.

## 5. Data & Mobile Phone (kb-019) Verification
1. We will verify the provided candidate `Mobile Phone` details against MeitY / BIS CRO official portals.
2. Verified claims will be compiled into the new detailed JSON schema format.
3. We will inject this single high-fidelity record into `knowledge_base.json` and ensure test suites (`test_phase5_product_coverage.py`) pass.

## 6. Validation Requirements
- `python -m pytest -q` must run clean (no regressions on the 179 established tests).
- Backend must correctly shape responses for legacy flat records and new structured records concurrently.
- No dummy/placeholder URLs (only `https://www.crsbis.in`, `https://www.bis.gov.in`, `https://www.meity.gov.in`).
- **Prerequisite logic**: Must visually trigger and link to an official service when a requirement status is MISSING.

---

> [!IMPORTANT]
> Please review this architectural approach. Once approved, I will proceed with extending the schema in `models.py`, updating `decision.py`, updating the frontend React components, and verifying the `kb-019` mobile phone record to test the new end-to-end Compliance Journey.
