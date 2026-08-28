"""
Loads the curated demo knowledge base and provides a simple
keyword-overlap retrieval function that stands in for a vector-DB
semantic search in this prototype. Swapping this module for a real
embeddings + vector store implementation (e.g. FAISS / Chroma) would
plug directly into the same interface used by rag.py.
"""
import json
import os
import re
from typing import List, Dict, Any

_KB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "knowledge_base.json")

_STOPWORDS = {
    "a", "an", "the", "is", "are", "what", "which", "how", "do", "does",
    "i", "my", "for", "of", "to", "in", "on", "and", "or", "can", "you",
    "please", "tell", "me", "about", "applies", "apply", "required",
    "need", "needed", "this", "that", "it", "your", "explain",
}


def _load_kb() -> List[Dict[str, Any]]:
    with open(_KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


_KB = _load_kb()


def _tokenize(text: str) -> List[str]:
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return [w for w in words if w not in _STOPWORDS and len(w) > 1]


def search(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Score each KB record by keyword + phrase overlap with the query."""
    query_lower = query.lower()
    tokens = set(_tokenize(query))
    scored = []

    for record in _KB:
        score = 0
        
        # 1. Exact title or standard number match (Very Strong)
        if record.get("title", "").lower() in query_lower:
            score += 20
        if record.get("standard_number", "").lower() in query_lower:
            score += 20
            
        # 2. Keyword exact match
        for kw in record.get("keywords", []):
            if kw.lower() in query_lower:
                score += 10
                
        # 3. Token overlap against keywords + title + topic
        haystack_tokens = set(_tokenize(" ".join(record.get("keywords", []))
                                         + " " + record.get("title", "")
                                         + " " + record.get("topic", "")))
        
        overlap = len(tokens & haystack_tokens)
        score += overlap * 2

        if score > 0:
            # Determine confidence
            if score >= 20:
                confidence = "high"
            elif score >= 10:
                confidence = "medium"
            elif score >= 4:
                confidence = "low"
            else:
                confidence = "none"
                
            if confidence != "none":
                # Copy record to avoid mutating global state and inject confidence
                r_copy = dict(record)
                r_copy["_retrieval_score"] = score
                r_copy["_retrieval_confidence"] = confidence
                scored.append((score, r_copy))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in scored[:top_k]]


def all_records() -> List[Dict[str, Any]]:
    return _KB


def get_by_topic_keyword(text: str, top_k: int = 3):
    return search(text, top_k=top_k)
