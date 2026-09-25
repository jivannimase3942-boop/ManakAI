# ManakAI - BIS Standards Decision and Action Assistant

**Smart India Hackathon 2026 | Problem Statement: SIH26107**

ManakAI is an AI-assisted decision and action system for discovering, understanding, and acting on BIS-related information.

> **Prototype Disclaimer**
>
> ManakAI is an independent hackathon prototype. It is not an official Bureau of Indian Standards (BIS) service and is not affiliated with or endorsed by BIS. It must not be used as a substitute for official BIS decisions, approvals, certifications, or legal/compliance advice. Always verify requirements with official BIS sources.

## The Problem

BIS standards and compliance information can be difficult for consumers, MSMEs, and industries to interpret and connect with their specific needs.

A conventional search experience primarily returns documents, links, and information. A generic conversational AI system can explain information but may produce unsupported or hallucinated standards, requirements, clauses, or sources.

The challenge is therefore not only **finding information**, but connecting a user's intent to **verified BIS information while preventing unsupported compliance decisions**.

## Our Approach

ManakAI combines conversational AI with deterministic retrieval and safety controls.

The LLM is deliberately limited to a **normalization layer**. It can assist with:

* Language normalization
* Entity extraction
* Query normalization
* Handling complex or multilingual natural-language queries

The LLM does **not** decide which BIS standard applies.

The final compliance-oriented response is controlled by deterministic application logic using:

* Intent Detection
* Keyword Retrieval
* Semantic Retrieval
* Hybrid Ranking
* Candidate Safety Gates
* Verified Knowledge Records
* Evidence-backed Responses
* `NO VERIFIED MATCH` handling

### Core Principle

> **Semantic similarity discovers candidates. Deterministic logic validates them.**

This separation is central to ManakAI's hallucination-resistant architecture.

## How ManakAI Works

```text
USER QUERY
    |
    v
OPTIONAL LLM NORMALIZATION
    |
    +-- Language normalization
    +-- Entity extraction
    +-- Query normalization
    |
    v
DETERMINISTIC INTENT ENGINE
    |
    +-- Requirements
    +-- Certification
    +-- Testing
    +-- Services
    +-- Other workflows
    |
    v
HYBRID RETRIEVAL ENGINE
    |
    +-- Keyword / lexical retrieval
    +-- Semantic retrieval
    |
    v
CANDIDATE SAFETY GATES
    |
    +-- Verified records only
    +-- Entity validation
    +-- State filtering
    +-- Reject invalid candidates
    |
    v
HYBRID RANKING
    |
    +-- Semantic similarity
    +-- Exact entity matching
    |
    v
SAFETY / CONFIDENCE GATE
    |
    +-----------------------------+
    |                             |
    v                             v
VERIFIED MATCH              NO VERIFIED MATCH
    |                             |
    v                             v
DETERMINISTIC DECISION       SAFE FALLBACK
ENGINE                         |
    |                           +-- Official BIS resources
    v
EVIDENCE-BACKED RESPONSE
    |
    +-- Decision Card
    +-- Why This Answer
    +-- Evidence
    +-- Compliance Journey
```

## Knowledge Base

ManakAI uses a structured verified knowledge base containing compliance-oriented records.

Each record can contain structured information such as:

* Product or service entity
* Applicable standard
* Requirements
* Testing information
* Certification steps
* Required documents
* Sources
* Verification state

The system does not treat an LLM-generated statement as authoritative evidence.

When sufficient verified evidence is unavailable, ManakAI does not invent an answer. It returns:

```text
NO VERIFIED MATCH
```

This is a deliberate safety outcome, not an application failure.

## Safety Architecture

ManakAI follows a defense-in-depth approach because incorrect compliance guidance can have real-world consequences.

### Verified Retrieval

Only verified knowledge records are eligible for live decision-making.

### State Filtering

Invalid or unsuitable records such as:

* `PENDING`
* `REJECTED`
* `SUPERSEDED`

are prevented from being used as authoritative matches.

### Evidence Thresholds

Semantic similarity alone cannot establish BIS applicability.

A candidate must pass deterministic validation and safety gates before a positive result is returned.

### Vague Query Rejection

Queries without enough product, service, or compliance context can result in `NO VERIFIED MATCH` rather than an unsupported recommendation.

### LLM Subordination

The LLM cannot:

* Override the decision engine
* Select an authoritative BIS standard by itself
* Invent official sources
* Create compliance evidence
* Bypass safety gates

If LLM normalization fails, the system can fall back to deterministic retrieval.

## Why ManakAI?

### Compared with conventional search

Search engines help users **find information**.

ManakAI attempts to connect the user's intent with verified BIS knowledge and present the result as an actionable, evidence-backed workflow.

### Compared with generic AI chatbots

A generic LLM can generate plausible-sounding answers even when evidence is insufficient.

ManakAI deliberately limits the LLM's authority.

The system prioritizes:

**Verified data > deterministic validation > evidence-backed response > conversational explanation**

rather than allowing generated text to become the source of truth.

## Key Features

| Feature                                | Status                 |
| -------------------------------------- | ---------------------- |
| Verified Multi-Category Knowledge Base | Implemented            |
| Required Document Guidance             | Implemented            |
| Know Before You Buy                    | Implemented            |
| Consumer Complaint Copilot             | Implemented            |
| MSME / Industry Compliance Copilot     | Implemented            |
| Smart Laboratory Guidance              | Implemented            |
| Official Source / Document Centre      | Implemented            |
| Multilingual Query Experience          | Implemented            |
| Voice Assistant                        | Implemented            |
| User Search History                    | Implemented            |
| Saved Standards / Products             | Implemented            |
| Guest User Experience                  | Implemented            |
| Login / Register Foundation            | Implemented / Deferred |
| User Dashboard                         | Implemented            |
| BIS Learning Centre                    | Implemented            |
| Quiz / Knowledge Test                  | Implemented            |
| Safety / No-Verified-Match Experience  | Implemented            |
| Evidence Chain                         | Implemented            |
| Responsive / Accessibility / UX        | Implemented            |

## Multilingual Experience

ManakAI is architecturally designed to process queries across multiple Indian languages, including:

* English
* Hindi
* Marathi
* Kannada
* Telugu
* Tamil
* Gujarati

The multilingual pipeline uses normalization and deterministic retrieval. If an external LLM provider is unavailable or rate-limited, the application can fall back to its deterministic retrieval path.

## Technology Stack

### Frontend

* React
* Vite
* Tailwind CSS
* Web Speech API
* Responsive component-based UI

### Backend

* Python
* FastAPI
* Deterministic decision engine
* Hybrid retrieval pipeline
* Structured compliance response models

### AI / Retrieval

* Optional LLM normalization
* Keyword / lexical retrieval
* Semantic retrieval
* Hybrid ranking
* Verified knowledge records

### Data

* Structured knowledge-base records
* Evidence/source metadata
* Local browser persistence for selected user features

## Repository Structure

```text
ManakAI/
│
├── backend/
│   └── app/
│       ├── decision.py
│       ├── embeddings.py
│       ├── hybrid_retriever.py
│       ├── intent.py
│       ├── knowledge_base.py
│       ├── llm.py
│       ├── models.py
│       ├── rag.py
│       ├── semantic_retriever.py
│       └── vision.py
│
├── frontend/
│
├── data/
│
├── docs/
│   ├── architecture/
│   ├── audits/
│   ├── demo/
│   ├── jury/
│   ├── product/
│   ├── roadmap/
│   └── technical/
│
├── tests/
│
└── README.md
```

## Documentation

Detailed project documentation is organized under `docs/`:

* `docs/architecture/` - System architecture, data flow, and AI safety
* `docs/audits/` - Feature and repository audits
* `docs/demo/` - Demo guides and demonstration queries
* `docs/jury/` - Jury cheat sheet and technical brief
* `docs/product/` - Product overview, feature status, and limitations
* `docs/roadmap/` - Product roadmap and future development
* `docs/technical/` - Technical overview and security documentation

## API

The backend exposes API functionality for health checks, assistant queries, standard search, services, and verified sources.

Refer to the backend implementation and technical documentation for the current API contract.

## Local Development

### Prerequisites

* Python 3.10+
* Node.js 18+
* npm

### Backend

From the project root:

```bash
cd backend
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI application using the project's configured application entry point.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The development server will display the local URL in the terminal.

## Environment Configuration

Create the required environment configuration from the provided example file when using optional external LLM functionality.

The LLM is not the authoritative source of compliance decisions. If the external normalization service is unavailable, the deterministic application path is designed to remain operational.

## Demonstration Queries

Example queries include:

```text
What BIS standard applies to packaged drinking water?

I manufacture packaged drinking water. What requirements do I need?

How can I apply for BIS certification?

Where can I test my product?

What is hallmarking?

Which BIS scheme applies to electronics?

How can a consumer verify HUID?

What documents are required for certification?
```

The project also contains a larger set of demonstration queries under:

```text
docs/demo/DEMO_QUERIES.md
```

## Limitations

ManakAI is a prototype and has defined limitations.

The current knowledge base is curated for the project's demonstration scope and is **not an exhaustive representation of all BIS standards**.

The system does not claim to replace official BIS systems, certification authorities, laboratories, or regulatory decisions.

External LLM providers may also impose availability and quota limitations. When normalization fails, deterministic fallback behavior is used where supported.

For detailed limitations, see:

```text
docs/product/LIMITATIONS.md
```

## Future Scope

Potential future development includes:

* Expansion of the verified knowledge base
* More extensive multilingual validation
* Improved semantic retrieval
* Automated verified data ingestion pipelines
* Stronger source/version tracking
* Integration with official BIS systems where appropriate and officially supported
* Expanded laboratory and certification workflows
* Production-grade authentication and persistence
* Larger-scale evaluation and retrieval benchmarking

## Project Status

ManakAI currently represents a functional hackathon prototype with an implemented frontend, FastAPI backend, deterministic decision engine, verified knowledge workflow, safety gates, evidence presentation, multilingual architecture, and supporting documentation.

The project prioritizes **traceability, deterministic validation, and safe failure over unrestricted AI generation**.

## Disclaimer

ManakAI is an independent technology prototype created for demonstration purposes.

It is not an official BIS service and is not affiliated with or endorsed by the Bureau of Indian Standards.

For actual standards, certification requirements, licences, laboratory information, fees, regulatory decisions, or other official matters, verify the information directly through official BIS channels.
