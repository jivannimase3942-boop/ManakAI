"""
Simple RAG pipeline for the ManakAI prototype.

    User query
      -> knowledge_base.search()   (keyword-overlap retrieval, stands in
                                     for embeddings + vector DB)
      -> if LLM configured: llm.generate() using retrieved context
      -> else: Demo Mode templated answer built from the retrieved record
      -> response always carries the source(s) used
"""
from typing import List, Dict, Any, Optional
from . import knowledge_base, llm

DISCLAIMERS = {
    "en": "This is a prototype demonstration for SIH 2026, not an official BIS service. Please verify final requirements with official BIS sources.",
    "hi": "यह SIH 2026 के लिए एक प्रोटोटाइप प्रदर्शन है, आधिकारिक BIS सेवा नहीं। कृपया अंतिम आवश्यकताओं की पुष्टि आधिकारिक BIS स्रोतों से करें।",
    "mr": "हे SIH 2026 साठी एक प्रोटोटाइप प्रात्यक्षिक आहे, अधिकृत BIS सेवा नाही. कृपया अंतिम आवश्यकतांची खातरजमा अधिकृत BIS स्त्रोतांकडून करा.",
}

NO_MATCH_TEXT = {
    "en": "I couldn't find a verified match for this in the ManakAI demo knowledge base. Please rephrase your question, or check the official BIS website (bis.gov.in) for authoritative information.",
    "hi": "मुझे ManakAI डेमो नॉलेज बेस में इसके लिए कोई सत्यापित जानकारी नहीं मिली। कृपया अपना प्रश्न दोबारा लिखें, या आधिकारिक जानकारी के लिए BIS वेबसाइट (bis.gov.in) देखें।",
    "mr": "मला ManakAI डेमो नॉलेज बेसमध्ये यासाठी सत्यापित माहिती सापडली नाही. कृपया तुमचा प्रश्न पुन्हा लिहा, किंवा अधिकृत माहितीसाठी BIS वेबसाइट (bis.gov.in) पहा.",
}

LANG_NAMES = {"en": "English", "hi": "Hindi", "mr": "Marathi"}


def _record_to_source(r: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "title": r["title"],
        "standard_number": r["standard_number"],
        "source_name": r["source_name"],
        "source_url": r["source_url"],
        "verified": r.get("verified", True),
    }


def _demo_answer(query: str, records: List[Dict[str, Any]], language: str) -> str:
    top = records[0]
    if language == "en":
        text = (
            f"Based on the ManakAI demo knowledge base, this relates to **{top['title']}**"
            f" ({top['standard_number']}).\n\n{top['summary']}\n\nGuidance: {top['guidance']}"
        )
    elif language == "hi":
        text = (
            f"ManakAI डेमो नॉलेज बेस के अनुसार, यह **{top['title']}** ({top['standard_number']}) से संबंधित है।\n\n"
            f"{top['summary']}\n\nमार्गदर्शन: {top['guidance']}\n\n"
            f"(नोट: यह उत्तर अंग्रेज़ी स्रोत डेटा से अनुवादित/सारांशित प्रोटोटाइप जानकारी है।)"
        )
    else:  # mr
        text = (
            f"ManakAI डेमो नॉलेज बेसनुसार, हे **{top['title']}** ({top['standard_number']}) शी संबंधित आहे.\n\n"
            f"{top['summary']}\n\nमार्गदर्शन: {top['guidance']}\n\n"
            f"(टीप: हे उत्तर इंग्रजी स्रोत डेटावरून भाषांतरित/सारांशित केलेली प्रोटोटाइप माहिती आहे.)"
        )
    return text


def _llm_answer(query: str, records: List[Dict[str, Any]], language: str) -> Optional[str]:
    context_blocks = []
    for r in records:
        context_blocks.append(
            f"Title: {r['title']}\nStandard: {r['standard_number']}\nSummary: {r['summary']}\n"
            f"Guidance: {r['guidance']}\nSource: {r['source_name']} ({r['source_url']})"
        )
    context = "\n\n---\n\n".join(context_blocks)

    lang_name = LANG_NAMES.get(language, "English")
    system_prompt = (
        "You are ManakAI, a demo assistant for an SIH 2026 hackathon prototype about Indian "
        "Standards and BIS services. You must answer ONLY using the provided context records. "
        "Never invent standard numbers, clauses, lab names, or certification requirements that "
        "are not present in the context. If the context does not fully answer the question, say "
        "so plainly and suggest checking the official BIS website. Keep answers concise (under "
        "150 words), clear, and in simple language for industries, MSMEs, students and consumers. "
        f"Respond in {lang_name}. Always make clear this is prototype/demo guidance, not an "
        "official BIS ruling."
    )
    user_prompt = f"Context records:\n\n{context}\n\nUser question: {query}"

    try:
        return llm.generate(system_prompt, user_prompt)
    except Exception:
        return None


def answer_query(query: str, language: str = "en") -> Dict[str, Any]:
    language = language if language in ("en", "hi", "mr") else "en"
    records = knowledge_base.search(query, top_k=3)

    if not records:
        return {
            "answer": NO_MATCH_TEXT[language],
            "matched_topic": None,
            "standard_number": None,
            "sources": [],
            "mode": "demo",
            "confidence": "none",
            "disclaimer": DISCLAIMERS[language],
        }

    mode = "demo"
    text = None

    if llm.is_llm_configured():
        text = _llm_answer(query, records, language)
        if text:
            mode = "llm"

    if not text:
        text = _demo_answer(query, records, language)
        mode = "demo"

    top = records[0]
    return {
        "answer": text,
        "matched_topic": top["topic"],
        "standard_number": top["standard_number"],
        "sources": [_record_to_source(r) for r in records],
        "mode": mode,
        "confidence": "high" if records[0] else "low",
        "disclaimer": DISCLAIMERS[language],
    }


def find_standard_for_product(description: str, language: str = "en") -> Optional[Dict[str, Any]]:
    language = language if language in ("en", "hi", "mr") else "en"
    records = knowledge_base.search(description, top_k=3)
    if not records:
        return None
    top = records[0]
    return {
        "title": top["title"],
        "standard_number": top["standard_number"],
        "topic": top["topic"],
        "summary": top["summary"],
        "guidance": top["guidance"],
        "sources": [_record_to_source(r) for r in records],
        "confidence": "high",
    }
