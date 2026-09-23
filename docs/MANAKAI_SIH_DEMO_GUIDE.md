# ManakAI SIH National-Level Demo Guide

## 1. Demo Objective
The goal of this demonstration is to prove that ManakAI securely and accurately navigates the complex space of BIS compliance. The demo must prove:
- **Natural-language BIS-related query understanding**: Recognizing intent from unstructured input.
- **Retrieval from controlled/verified knowledge**: Sourcing exclusively from a curated knowledge base.
- **Deterministic safety validation**: Ensuring AI guesses are blocked by mathematical thresholds and strict logic gates.
- **Evidence-backed response**: Linking all claims directly to official sources.
- **Compliance guidance**: Presenting complex procedures as an actionable journey.
- **Safe NO VERIFIED MATCH behaviour**: Demonstrating deliberate hallucination resistance when evidence is lacking.

---

## 2. 5–8 Minute Demo Flow
1. **Problem** (30–45 sec)
2. **Solution** (30 sec)
3. **Architecture** (45 sec)
4. **Live Demo** (3–4 min)
5. **Safety / hallucination demonstration** (45 sec)
6. **AI architecture explanation** (45 sec)
7. **Differentiation + impact** (30 sec)
8. **Closing** (15–20 sec)

---

## 3. Opening Script
**The Problem**:
"Users often know exactly what product they want to manufacture, import, certify, or test, but they do not know which specific bureaucratic BIS standard, scheme, or service pathway is relevant to them."

**The Solution**:
"ManakAI converts a natural-language compliance question into a structured guidance response. It provides applicable verified information, official evidence, and next actions where supported."

*(Note for Presenter: Do NOT claim ManakAI is an official BIS service.)*
**Disclaimer to state**:
"ManakAI is an independent technology prototype providing AI-assisted guidance based on publicly available BIS information. For official decisions and services, please refer to BIS."

---

## 4. Architecture Explanation
**Flow**:
User Query → Query Normalization → Intent Detection → Deterministic + Semantic Retrieval → Candidate Gating → Hybrid Ranking → Safety / Confidence Gate → Deterministic Decision Engine → Evidence-backed Compliance Response → Frontend UI

**Key Concept**:
"Semantic similarity is used purely for candidate discovery, NOT as proof of applicability. The final decision remains strictly controlled by deterministic validation and safety gates."

---

## 5. Live Demo Queries & Scripts

### A. Packaged drinking water
- **Query**: "What standard applies to packaged drinking water?"
- **Expected Result**: IS 14543 / positive verified match.
- **Point To**: The `DecisionCard` showing the standard, and the `ComplianceJourney` outlining the testing steps.
- **Say**: "Notice how it extracts the exact product and maps it to IS 14543, providing a clear breakdown of the testing and certification journey."
- **Technical**: Demonstrates intent mapping (REQUIREMENTS) and hybrid semantic matching.
- **DO NOT CLAIM**: That this represents the *entire* exhaustive legal requirement (it is a curated prototype response).

### B. Cement
- **Query**: "Which BIS standard is used for cement?"
- **Expected Result**: IS 269 (where supported in the knowledge base).
- **Point To**: The `WhyThisAnswer` accordion showing transparency in the decision.
- **Say**: "Here, the system explains exactly why it chose this standard based on the verified backend record."
- **Technical**: Shows adaptability to different sentence structures.
- **DO NOT CLAIM**: That it covers every niche variant of cement.

### C. Laptop
- **Query**: "What BIS standard applies to laptops?"
- **Expected Result**: IS 13252 Part 1 / CRS scheme mapping.
- **Point To**: The Scheme identifier showing CRS instead of ISI.
- **Say**: "ManakAI correctly identifies that electronics fall under the Compulsory Registration Scheme (CRS) rather than standard ISI certification."
- **Technical**: Proves the system handles complex compliance scheme variations.
- **DO NOT CLAIM**: That every laptop automatically has the identical compliance path.

### D. Generic certification
- **Query**: "I need BIS certification."
- **Expected Result**: `NO VERIFIED MATCH`.
- **Point To**: The "NO VERIFIED BIS MATCH" warning and next steps.
- **Say**: "Because no specific product was mentioned, the system deliberately refuses to force a specific standard and instead asks for specificity."
- **Technical**: Demonstrates safety against vague entity extraction.

### E. Testing laboratory
- **Query**: "I need a BIS testing laboratory."
- **Expected Result**: `NO VERIFIED MATCH`.
- **Point To**: The absence of a hallucinated laboratory address.
- **Say**: "The system does not invent a laboratory recommendation when it does not have sufficiently verified evidence in the current dataset."
- **Technical**: Shows safe handling of out-of-scope intents.

### F. Aircraft certification (Safety Demo)
- **Query**: "What BIS standard applies to aircraft certification?"
- **Expected Result**: `NO VERIFIED MATCH`.
- **Point To**: The immediate safe refusal.
- **Say**: "The system has no verified applicable record for this query in the current supported knowledge base, so it refuses to fabricate a standard."
- **Technical**: Deliberate safety behavior showing the confidence threshold actively blocking an unsupported domain.

### G. Unknown product
- **Query**: "What is the standard for unobtainium?" (or similar unsupported query)
- **Expected Result**: `NO VERIFIED MATCH`.
- **Point To**: The safe refusal UI.
- **Say**: "Absence of evidence results in a safe refusal, never a hallucination."

### H. Hindi
- **Query**: "लैपटॉप के लिए कौन सा मानक लागू होता है?"
- **Expected Result**: Verified match (if API quota permits) or NO VERIFIED MATCH.
- **Say**: "Multilingual processing is architecturally supported and undergoing live validation."
- **Technical**: Uses the LLM normalizer to translate intent before deterministic retrieval. (If it fails, state honestly that Gemini API quotas limited live throughput).

### I. Marathi
- **Query**: "सिमेंटसाठी कोणता BIS मानक वापरला जातो?"
- **Expected Result**: Verified match (if API quota permits) or NO VERIFIED MATCH.
- **Say**: "Just like Hindi, Marathi is supported through our normalizer layer, demonstrating regional accessibility."
- **DO NOT CLAIM**: 100% real-world multilingual accuracy.

---

## 6. Safety Demonstration Focus
When executing the aircraft certification (Scenario F) or unknown product (Scenario G) queries:
- Emphasize: "No verified applicable record → NO VERIFIED MATCH."
- Explain: "This is not a system failure. It is a deliberate refusal to fabricate an answer. In compliance, a refusal is safer than a guess."

---

## 7. "Is this just an LLM wrapper?"
**Answer**: "No. The LLM is only used for controlled query normalization. It does not directly select the BIS standard. The standard must come from the controlled knowledge base and pass retrieval, candidate gating, and deterministic safety validation."

---

## 8. "How do you prevent hallucination?"
**Answer**: We prevent hallucination through a strict pipeline:
- **Controlled Knowledge Base**: Sourcing only verified data.
- **Verification States**: Blocking PENDING/REJECTED records.
- **Candidate Gating & Safety Thresholds**: Mathematically restricting semantic similarity.
- **Deterministic Decision Engine**: Overriding LLM suggestions if evidence is lacking.
- **NO VERIFIED MATCH**: Refusing to guess when confidence is insufficient.

---

## 9. Differentiation from BIS Website
**Answer**: "BIS already provides official information and services. ManakAI focuses on the guidance layer — helping users convert a natural language question into a structured path toward relevant standard information, evidence, and next actions."

---

## 10. Differentiation from a Generic Chatbot
**Answer**:
- **Generic Chatbot**: Question → Generated Answer (Prone to legal hallucinations).
- **ManakAI**: Question → Intent → Controlled Retrieval → Candidate Validation → Safety Gate → Deterministic Decision → Evidence-backed Guidance.

---

## 11. Multilingual Explanation
**Answer**: "Multilingual processing is architecturally supported and undergoing live validation."
*(If pressed: Explain that live LLM normalization relies on provider availability, and previous HTTP 429 errors from the Gemini API restricted live throughput, demonstrating our safe fallback mechanisms).*

---

## 12. Demo Failure Recovery

| Failure Scenario | What to Do | What to Say | What NOT to Do |
| :--- | :--- | :--- | :--- |
| **Backend unavailable** | Wait 30s (Render cold start) | "Our backend spins up on demand to save resources; it just needs a few seconds." | Panic or hide the issue. |
| **Frontend unavailable** | Refresh the Vercel URL | "A slight network hiccup, let me refresh." | Blame the local machine entirely. |
| **LLM HTTP 429 / Quota** | Fallback to English query | "Our normalization provider is rate-limiting us, so the system safely rejected the query. Let me show you the English deterministic equivalent." | Hide the error or fake the translation. |
| **Multilingual failure** | Explain safe fallback | "Notice how the system safely returned 'No Match' rather than mistranslating compliance advice." | Try to force it to work repeatedly. |
| **Unexpected NO MATCH** | Check query spelling | "The safety gate is incredibly strict; even a slight ambiguity triggers a safe refusal." | Apologize for a "bug". It's a feature. |
| **Network failure** | Use backup screenshots | "Since internet is down, let me walk you through the architectural screenshots we prepared." | Keep clicking refresh endlessly. |

---

## 13. Final Closing Script
"ManakAI demonstrates that AI-assisted guidance can be safe, explainable, and rooted purely in verified evidence. By prioritizing deterministic safety over generative guessing, we've built a scalable prototype that bridges the gap between natural language questions and official BIS compliance pathways."

---

## 14. Presenter Checklist

**BEFORE DEMO:**
- [ ] Frontend loaded
- [ ] Backend responding (Render cold start resolved)
- [ ] Demo queries prepared & copied
- [ ] Browser ready and zoom checked
- [ ] Disclaimer visible
- [ ] Architecture diagram available
- [ ] Backup screenshots prepared
- [ ] No secrets or `.env` visible
- [ ] Correct deployment branch checked

**DURING DEMO:**
- [ ] Explain the result, not just the UI
- [ ] Point explicitly to the Evidence and URL
- [ ] Demonstrate safe refusal (`NO VERIFIED MATCH`)
- [ ] Do not claim unsupported functionality

**AFTER DEMO:**
- [ ] Explain limitations honestly
- [ ] Answer technical questions concisely
- [ ] Explain roadmap scaling
