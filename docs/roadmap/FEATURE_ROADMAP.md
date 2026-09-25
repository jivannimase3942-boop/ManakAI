# ManakAI Feature Expansion Roadmap

## 1. Current Capabilities
ManakAI is built on a highly secure, deterministic retrieval architecture that incorporates AI for intent understanding without surrendering decision-making authority.
- **Implemented & Verified**: AI BIS Assistant, Intent Detection, Keyword/Semantic/Hybrid Retrieval, Safety Gates, Evidence Architecture, Multilingual Normalization (LLM), and a robust Phase 3A React UI (`DecisionCard`, `ComplianceJourney`, `NoVerifiedMatch`).
- **Core Principle**: Semantic similarity discovers candidates; deterministic logic validates them.

## 2. Original Requested Feature List
**Tier A — Core Demo Features**
1. AI BIS Assistant
2. Intelligent Intent Detection
3. Multi-category BIS Knowledge Base
4. Evidence / Source-backed Answers
5. Required Documents / Document Guidance
6. Smart Laboratory Finder
7. MSME / Industry Compliance Copilot
8. Know Before You Buy
9. Compliance Readiness Score
10. Multilingual AI

**Tier B — Advanced Demo Features**
11. Scan & Verify
12. Licence Verification
13. HUID Verification
14. R-number / CRS Verification
15. AI Fraud / Misuse Risk Detection
16. Safety Alerts / Product Recall
17. Complaint Copilot

**Tier C — User Platform**
18. Login/Register
19. User Dashboard
20. Saved Standards/Products
21. Query History
22. My Complaints
23. Notifications

**Tier D — Experience**
24. Voice Assistant
25. BIS Learning
26. Quiz / Knowledge Test

---

## 3 & 4. Feature-by-Feature Audit & Priority Classification

### Tier A (Core)
**3. Multi-category BIS Knowledge Base**
- **Current status**: Limited benchmark data (13 records).
- **Demo value / User value**: HIGH / HIGH.
- **Technical complexity**: Low (schema exists, requires JSON expansion).
- **Data requirement**: Verified official sources for toys, electronics, helmets, etc.
- **Priority**: **P1** (Expand selectively for demo variety).

**5. Required Documents / Document Guidance**
- **Current status**: Not implemented.
- **Demo value / User value**: HIGH / HIGH.
- **Technical complexity**: Medium (requires modifying JSON schema to include `required_documents`).
- **Data requirement**: Verified BIS document checklists.
- **Priority**: **P1** (Can be implemented immediately using existing UI loops).

**6. Smart Laboratory Finder**
- **Current status**: Not implemented.
- **Demo value / User value**: HIGH / HIGH.
- **Technical complexity**: High (Laboratory mapping is vast and dynamic).
- **Data requirement**: Massive official BIS lab registry.
- **Priority**: **P4** (Do NOT build unless static verified subset is provided. Fake lab data is a severe safety risk).

**7. MSME / Industry Compliance Copilot**
- **Current status**: Partially covered by `ComplianceJourney`.
- **Demo value / User value**: HIGH / HIGH.
- **Technical complexity**: Low (Extends existing intent parser).
- **Priority**: **P2** (Reuse core architecture to frame responses for MSMEs).

**8. Know Before You Buy (Consumer)**
- **Current status**: Not implemented.
- **Demo value / User value**: HIGH / HIGH.
- **Priority**: **P2** (Requires adding "consumer_checks" array to JSON schema and UI).

**9. Compliance Readiness Score**
- **Current status**: Not implemented.
- **Priority**: **P4** (Do not build. Faking a percentage score is unsafe. Prefer simple checklist counts).

**10. Multilingual AI**
- **Current status**: LLM normalization implemented; live evaluation limited by API quotas.
- **Priority**: **P1** (Critical for SIH narrative, but bound by external constraints).

### Tier B (Advanced Verification)
**11-14. Scan & Verify / Licence / HUID / CRS**
- **Current status**: Not implemented.
- **Technical complexity**: Extremely High.
- **Data requirement**: Live connection to protected BIS databases.
- **Priority**: **P4** (Do not fake live verification. Can only provide an official-source redirect link unless an official public API is provided).

**15. AI Fraud / Misuse Risk Detection**
- **Current status**: Not implemented.
- **Priority**: **P4** (Requires massive external data to cross-reference claims safely. Too legally sensitive for a prototype).

**16. Safety Alerts / Product Recall**
- **Current status**: Not implemented.
- **Priority**: **P4** (Requires live official feed).

**17. Complaint Copilot**
- **Current status**: Not implemented.
- **Demo value / User value**: HIGH / HIGH.
- **Priority**: **P2** (Can be implemented as structured guidance/checklist to help draft a complaint, but MUST redirect to official portal for actual filing).

### Tier C (User Platform)
**18-23. Login / Dashboard / History / Saved Items**
- **Current status**: Not implemented.
- **Priority**: **P3** (Local storage session history is P2. Avoid heavy DB/Auth for the prototype as it dilutes focus from AI retrieval).

### Tier D (Experience)
**24-26. Voice Assistant / Learning / Quiz**
- **Current status**: Not implemented.
- **Priority**: **P3 / P4** (Distraction from core compliance objective).

---

## 5. Recommended Implementation Order
1. **Expand Knowledge Base (P1)**: Add 5-10 verified records for highly recognizable categories (helmets, toys, pressure cookers).
2. **Required Documents Guidance (P1)**: Add structured document checklists to the expanded records and render them in the UI.
3. **Consumer Guidance "Know Before You Buy" (P2)**: Add consumer check arrays to the UI.
4. **Complaint Copilot Drafts (P2)**: Add intent detection for complaints and provide structured drafting/redirection guidance.
5. **Session History (P2/P3)**: Lightweight `localStorage` frontend history to demonstrate continuity.

---

## 6. Data/Source Requirements
All P1 and P2 features require structured extraction from official BIS PDFs or portals into the `knowledge_base.json`. **No web scraping of protected portals.**

## 7. Architecture Impact
The recommended features require **zero changes** to the core retrieval algorithms (`semantic_retriever.py`, `hybrid_retriever.py`, `decision.py`). They only require:
- Expanding the Pydantic schemas in `models.py`.
- Expanding the `knowledge_base.json` entries.
- Adding corresponding React UI blocks to `ComplianceJourney.jsx` or new sibling components.

## 8. Security Risks
- **Hallucination Risk**: Must ensure the LLM is NOT used to generate document lists or complaint pathways. All lists must be strictly parsed from the deterministic backend JSON.
- **Liability Risk**: Explicit warnings must surround "Complaint Drafting" and "Consumer Guidance" stating it is unofficial guidance.

## 9. Demo Value
By implementing Document Guidance and Consumer Checks, the demo transitions from a "Search Engine" to a true "Copilot," proving immense value for both MSMEs and consumers without faking live verifications.

## 10. Features That Must NOT Be Faked (P4)
- Live Licence / HUID / CRS Verification (Redirect only).
- Smart Laboratory Finder (Unless a static verified subset is explicitly provided).
- Compliance Readiness Percentage Scores.
- Fraud Detection labeling.

## 11. Features That Can Be Implemented Immediately
- Knowledge Base Category Expansion.
- Required Documents List UI.
- "Know Before You Buy" Consumer UI.
- Complaint Copilot Guidance (Drafting checklist + Official redirect).

## 12. Features Requiring Official Data/Integration
- Live Verification (HUID/Licence).
- Laboratory Database.
- Safety Alerts/Recalls.

## 13. Features to Defer
- Authentication, MongoDB/PostgreSQL, Notifications, Voice Assistant.

## 14. Proposed Milestone Plan

**Milestone 3B.3: Data Expansion**
- Expand `knowledge_base.json` with helmets, toys, steel.
- Add `required_documents` and `consumer_checks` schema fields.

**Milestone 3B.4: UI Copilot Expansion**
- Update UI to render documents and consumer checks safely.
- Implement Complaint Intent routing.

**Milestone 3B.5: Demo Polish**
- Implement `localStorage` lightweight session history.
- Final UI styling pass.
- Final automated test verification.
