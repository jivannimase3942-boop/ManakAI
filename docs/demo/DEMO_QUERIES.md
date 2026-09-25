# ManakAI Demo Queries

This document outlines the exact queries to be used during the SIH 2026 National-Level Demonstration.

## 1. Packaged drinking water
- **Query**: "What standard applies to packaged drinking water?"
- **Category**: Standard Identification (Core Feature)
- **Expected result**: Positive verified match (IS 14543), full `ComplianceJourney` (Testing, Certification steps).
- **Why it is included**: Demonstrates the primary happy path and structured journey parsing.
- **Current validation status**: IMPLEMENTED / VALIDATED

## 2. Cement
- **Query**: "Which BIS standard is used for cement?"
- **Category**: Standard Identification
- **Expected result**: Positive verified match for Cement (IS 269 if supported in KB).
- **Why it is included**: Demonstrates semantic flexibility ("Which BIS standard is used for...").
- **Current validation status**: IMPLEMENTED / VALIDATED

## 3. Laptop
- **Query**: "What BIS standard applies to laptops?"
- **Category**: CRS Scheme Mapping
- **Expected result**: Positive verified match for CRS scheme (kb-012 mapping).
- **Why it is included**: Proves the system handles different schemes (CRS vs ISI mark).
- **Current validation status**: IMPLEMENTED / VALIDATED

## 4. Certification
- **Query**: "I need BIS certification."
- **Category**: Vague Intent Rejection
- **Expected result**: `NO VERIFIED MATCH`
- **Why it is included**: Demonstrates that the system safely refuses to invent a standard when a specific product/entity is missing.
- **Current validation status**: EXPECTED SAFE FAILURE

## 5. Testing
- **Query**: "I need a BIS testing laboratory."
- **Category**: Unsupported / Vague Request
- **Expected result**: `NO VERIFIED MATCH`
- **Why it is included**: Proves the system will not invent a laboratory or fake external data when evidence is insufficient.
- **Current validation status**: EXPECTED SAFE FAILURE

## 6. Aircraft certification
- **Query**: "What BIS standard applies to aircraft certification?"
- **Category**: Out-of-Domain Safety
- **Expected result**: `NO VERIFIED MATCH`
- **Why it is included**: Essential demonstration of hallucination resistance. The system blocks the unknown domain rather than guessing.
- **Current validation status**: EXPECTED SAFE FAILURE

## 7. Random unknown product
- **Query**: "What is the standard for unobtainium?" (or similar arbitrary string)
- **Category**: Unknown Entity Rejection
- **Expected result**: `NO VERIFIED MATCH`
- **Why it is included**: Proves absence of evidence results in a safe refusal.
- **Current validation status**: EXPECTED SAFE FAILURE

## 8. Hindi Query
- **Query**: "लैपटॉप के लिए कौन सा मानक लागू होता है?" (What standard applies to laptops?)
- **Category**: Multilingual Processing
- **Expected result**: Positive verified match (if Gemini API is available) OR `NO VERIFIED MATCH` (if API quota is exhausted).
- **Why it is included**: Demonstrates architectural support for regional languages.
- **Current validation status**: IMPLEMENTED / NOT LIVE-VALIDATED (Subject to HTTP 429 Quotas)

## 9. Marathi Query
- **Query**: "सिमेंटसाठी कोणता BIS मानक वापरला जातो?" (Which BIS standard is used for cement?)
- **Category**: Multilingual Processing
- **Expected result**: Positive verified match (if API available) OR `NO VERIFIED MATCH` (if API quota is exhausted).
- **Why it is included**: Demonstrates regional language handling capabilities.
- **Current validation status**: IMPLEMENTED / NOT LIVE-VALIDATED (Subject to HTTP 429 Quotas)
