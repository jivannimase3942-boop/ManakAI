# ManakAI Product Overview

## 1. What is ManakAI?

ManakAI is an AI-assisted BIS Standards Decision and Action Assistant designed for industries, MSMEs, and consumers.

The system helps users understand relevant BIS information and identify practical next steps instead of simply returning a list of documents or search results.

## 2. Problem

BIS-related information can be difficult for non-expert users to interpret.

Users may need to determine:

- Which standard or requirement may apply to their product.
- What certification or compliance process may be relevant.
- What documents or testing information may be required.
- Where relevant BIS-related services or information can be found.
- How to understand a requirement before taking the next action.

Traditional search interfaces primarily return information. Generic AI systems may provide fluent answers but can introduce unsupported or hallucinated compliance information.

## 3. Proposed Solution

ManakAI combines deterministic application logic, verified knowledge records, hybrid retrieval, safety gates, and an optional LLM normalization layer.

The LLM does not independently decide which BIS requirement applies.

Instead, the system follows a controlled flow:

```text
User Query
    |
    v
Query Normalization
    |
    v
Intent Detection
    |
    v
Knowledge Retrieval
    |
    v
Candidate Validation
    |
    v
Confidence / Safety Gate
    |
    v
Decision Engine
    |
    v
Evidence-Backed Response