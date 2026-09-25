# ManakAI System Architecture

## 1. Architecture Overview

ManakAI is an independent technology prototype providing AI-assisted guidance based on publicly available BIS information.

The system separates conversational AI from compliance decision-making. The LLM is used as a normalization layer, while retrieval, verification, safety gates, and final compliance responses remain controlled by deterministic application logic.

> **Prototype disclaimer:** ManakAI is not an official BIS service and is not affiliated with or endorsed by the Bureau of Indian Standards. Official decisions and services should be verified through BIS.

## 2. Core Architecture

```text
USER / UI
    |
    v
React + Vite Frontend
    |
    v
FastAPI Backend
    |
    v
Optional LLM Normalizer
    |
    +-- Language normalization
    +-- Entity extraction
    +-- Query normalization
    |
    v
Deterministic Intent Engine
    |
    +-- Requirements
    +-- Certification
    +-- Services
    +-- Other workflows
    |
    v
Hybrid Retrieval Engine
    |
    +-- Lexical / Keyword Retrieval
    +-- Semantic Embedding Retrieval
    |
    v
Candidate Gating
    |
    +-- Invalid records
    +-- Unverified records
    +-- PENDING
    +-- REJECTED
    +-- SUPERSEDED
    |
    v
Hybrid Ranking
    |
    +-- Vector similarity
    +-- Exact entity matching
    |
    v
Safety / Confidence Gate
    |
    v
Deterministic Decision Engine
    |
    v
Evidence-Backed Compliance Response
    |
    +-- DecisionCard
    +-- WhyThisAnswer
    +-- EvidencePanel
    +-- ComplianceJourney