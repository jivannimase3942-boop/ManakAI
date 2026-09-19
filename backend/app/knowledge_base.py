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
    "क्या", "मैं", "किसी", "में", "करवा", "सकता", "हूं", "है",
    "मी", "करू", "शकतो", "का", "आहे", "काय", "कोणता", "साठी", "लागू",
    "के", "लिए", "से", "को", "कौन", "सा", "कहां", "कोणते"
}


def _load_kb() -> List[Dict[str, Any]]:
    with open(_KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


_KB = _load_kb()


import string

def _tokenize(text: str) -> List[str]:
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.lower().split()
    return [w for w in words if w not in _STOPWORDS and len(w) > 1]


def search(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Score each KB record by keyword + phrase overlap with the query."""
    query_lower = query.lower()
    tokens = set(_tokenize(query))
    scored = []

    for record in _KB:
        status = record.get("verification_status")
        if status in ["PENDING", "SUPERSEDED", "REJECTED"]:
            continue

        score = 0

        # 1. Exact title, product name, or standard number match (Very Strong)
        title = record.get("title", "").lower()
        if title and title in query_lower:
            score += 20
        product_name = record.get("product_name", "").lower()
        if product_name and product_name in query_lower:
            score += 20
        std_num = record.get("standard_number", "").lower()
        std_num_base = std_num.split(":")[0].strip() if std_num else ""
        if std_num and (std_num in query_lower or (std_num_base and std_num_base in query_lower)):
            score += 20

        # 1.5 i18n localized title matches
        i18n = record.get("i18n", {})
        for lang, l_data in i18n.items():
            loc_title = l_data.get("title", "").lower()
            if loc_title and loc_title in query_lower:
                score += 20
                break # Avoid adding multiple times for identical localized titles

        # 1.7 Root and i18n aliases (Very Strong match)
        for alias in record.get("aliases", []):
            if alias and alias.lower() in query_lower:
                score += 20
                break

        for lang, l_data in i18n.items():
            alias_matched = False
            for alias in l_data.get("aliases", []):
                if alias and alias.lower() in query_lower:
                    score += 20
                    alias_matched = True
                    break
            if alias_matched:
                break

        # 2. Keyword exact match
        matched_kws = set()
        for kw in record.get("keywords", []):
            if not kw: continue
            kw_lower = kw.lower()
            if kw_lower in query_lower and kw_lower not in matched_kws:
                score += 10
                matched_kws.add(kw_lower)

        for lang, l_data in i18n.items():
            for kw in l_data.get("keywords", []):
                if not kw: continue
                kw_lower = kw.lower()
                if kw_lower in query_lower and kw_lower not in matched_kws:
                    score += 10
                    matched_kws.add(kw_lower)
            for alias in l_data.get("aliases", []):
                if not alias: continue
                alias_lower = alias.lower()
                if alias_lower in query_lower and alias_lower not in matched_kws:
                    score += 10
                    matched_kws.add(alias_lower)

        # 3. Token overlap against keywords + title + topic + i18n
        haystack_texts = [
            " ".join(record.get("keywords", [])),
            record.get("title", ""),
            record.get("topic", "")
        ]
        for lang, l_data in i18n.items():
            haystack_texts.append(l_data.get("title", ""))
            haystack_texts.append(" ".join(l_data.get("keywords", [])))
            haystack_texts.append(" ".join(l_data.get("aliases", [])))

        haystack_tokens = set(_tokenize(" ".join(haystack_texts)))

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
