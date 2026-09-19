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
import os
from . import knowledge_base, llm, hybrid_retriever, intent

USE_HYBRID_RETRIEVAL = os.getenv("USE_HYBRID_RETRIEVAL", "true").lower() == "true"

def _is_bis_scope(query: str) -> bool:
    """Phase 8: BIS-Only Scope Control"""
    q = query.lower()
    bis_keywords = [
        "bis", "standard", "is ", "is-", "certification", "isi", "scheme",
        "hallmark", "huid", "lab", "testing", "crs", "licence", "license",
        "compliance", "complaint", "grievance", "pressure cooker", "toy",
        "cement", "laptop", "helmet", "water", "product", "mandatory",
        "voluntary", "guidance", "mobile", "phone", "smartphone", "power bank"
    ]
    # Simple deterministic check: if any keyword is present, allow it.
    for kw in bis_keywords:
        if kw in q:
            return True

    # Also allow hindi/marathi queries if they match basic patterns or are non-ascii
    if not all(ord(c) < 128 for c in q):
        return True

    return False

SCOPE_REJECT_TEXT = {
    "en": "ManakAI currently provides guidance related to BIS standards and services.",
    "hi": "ManakAI वर्तमान में BIS मानकों और सेवाओं से संबंधित मार्गदर्शन प्रदान करता है।",
    "mr": "ManakAI सध्या BIS मानके आणि सेवांशी संबंधित मार्गदर्शन प्रदान करते."
}


DISCLAIMERS = {
    "en": "ManakAI is an independent technology prototype providing AI-assisted guidance based on publicly available BIS information. For official decisions and services, please refer to BIS.",
    "hi": "ManakAI एक स्वतंत्र प्रौद्योगिकी प्रोटोटाइप है जो सार्वजनिक रूप से उपलब्ध BIS जानकारी के आधार पर AI-सहायता प्राप्त मार्गदर्शन प्रदान करता है। आधिकारिक निर्णयों और सेवाओं के लिए, कृपया BIS देखें।",
    "mr": "ManakAI हा एक स्वतंत्र तंत्रज्ञान प्रोटोटाइप आहे जो सार्वजनिकरीत्या उपलब्ध BIS माहितीवर आधारित AI-सहाय्यित मार्गदर्शन प्रदान करतो. अधिकृत निर्णय आणि सेवांसाठी, कृपया BIS पहा.",
    "kn": "ManakAI ಒಂದು ಸ್ವತಂತ್ರ ತಂತ್ರಜ್ಞಾನದ ಪ್ರೋಟೋಟೈಪ್ ಆಗಿದ್ದು, ಸಾರ್ವಜನಿಕವಾಗಿ ಲಭ್ಯವಿರುವ BIS ಮಾಹಿತಿಯನ್ನು ಆಧರಿಸಿ AI ನೆರವಿನ ಮಾರ್ಗದರ್ಶನವನ್ನು ಒದಗಿಸುತ್ತದೆ. ಅಧಿಕೃತ ನಿರ್ಧಾರಗಳು ಮತ್ತು ಸೇವೆಗಳಿಗಾಗಿ, ದಯವಿಟ್ಟು BIS ಅನ್ನು ನೋಡಿ.",
    "te": "ManakAI అనేది పబ్లిక్‌గా అందుబాటులో ఉన్న BIS సమాచారం ఆధారంగా AI-సహాయక మార్గదర్శకత్వాన్ని అందించే స్వతంత్ర సాంకేతిక నమూనా. అధికారిక నిర్ణయాలు మరియు సేవల కోసం, దయచేసి BISని చూడండి.",
    "ta": "ManakAI என்பது பொதுவில் கிடைக்கும் BIS தகவல்களின் அடிப்படையில் AI உதவியுடன் வழிகாட்டுதலை வழங்கும் ஒரு சுயாதீன தொழில்நுட்ப முன்மாதிரி ஆகும். அதிகாரப்பூர்வ முடிவுகள் மற்றும் சேவைகளுக்கு, BIS ஐப் பார்க்கவும்.",
    "gu": "ManakAI એક સ્વતંત્ર ટેકનોલોજી પ્રોટોટાઇપ છે જે સાર્વજનિક રીતે ઉપલબ્ધ BIS માહિતીના આધારે AI-સહાયિત માર્ગદર્શન પ્રદાન કરે છે. અધિકૃત નિર્ણયો અને સેવાઓ માટે, કૃપા કરીને BIS નો સંદર્ભ લો.",
}

NO_MATCH_TEXT = {
    "en": "I couldn't find a verified match for this in the ManakAI knowledge base. Please rephrase your question, or check the official BIS website (bis.gov.in) for authoritative information.",
    "hi": "मुझे ManakAI नॉलेज बेस में इसके लिए कोई सत्यापित जानकारी नहीं मिली। कृपया अपना प्रश्न दोबारा लिखें, या आधिकारिक जानकारी के लिए BIS वेबसाइट (bis.gov.in) देखें।",
    "mr": "मला ManakAI नॉलेज बेसमध्ये यासाठी सत्यापित माहिती सापडली नाही. कृपया तुमचा प्रश्न पुन्हा लिहा, किंवा अधिकृत माहितीसाठी BIS वेबसाइट (bis.gov.in) पहा.",
    "kn": "ManakAI ಡೆಮೊ ಜ್ಞಾನದ ಮೂಲದಲ್ಲಿ ಇದಕ್ಕಾಗಿ ನನಗೆ ಪರಿಶೀಲಿಸಿದ ಹೊಂದಾಣಿಕೆ ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಮರುಹೇಳಿ ಅಥವಾ ಅಧಿಕೃತ ಮಾಹಿತಿಗಾಗಿ BIS ವೆಬ್‌ಸೈಟ್ (bis.gov.in) ಪರಿಶೀಲಿಸಿ.",
    "te": "ManakAI డెమో నాలెడ్జ్ బేస్‌లో దీని కోసం నాకు ధృవీకరించబడిన సరిపోలిక కనుగొనబడలేదు. దయచేసి మీ ప్రశ్నను తిరిగి వ్రాయండి లేదా అధికారిక సమాచారం కోసం BIS వెబ్‌సైట్ (bis.gov.in) ను తనిఖీ చేయండి.",
    "ta": "ManakAI டெமோ அறிவுத் தளத்தில் இதற்கான சரிபார்க்கப்பட்ட பொருத்தம் எனக்குக் கிடைக்கவில்லை. தயவுசெய்து உங்கள் கேள்வியை மீண்டும் எழுதவும், அல்லது அதிகாரப்பூர்வ தகவலுக்கு BIS இணையதளத்தை (bis.gov.in) சரிபார்க்கவும்.",
    "gu": "મને ManakAI ડેમો નોલેજ બેઝમાં આના માટે કોઈ ચકાસાયેલ મેળ મળ્યો નથી. કૃપા કરીને તમારો પ્રશ્ન ફરીથી લખો, અથવા અધિકૃત માહિતી માટે BIS વેબસાઇટ (bis.gov.in) તપાસો.",
}

LANG_NAMES = {"en": "English", "hi": "Hindi", "mr": "Marathi", "kn": "Kannada", "te": "Telugu", "ta": "Tamil", "gu": "Gujarati"}


def _record_to_source(r: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": r.get("id"),
        "title": r["title"],
        "standard_number": r["standard_number"],
        "source_name": r["source_name"],
        "source_url": r["source_url"],
        "verified": r.get("verified", True),
    }


def _demo_answer(query: str, records: List[Dict[str, Any]], language: str) -> str:
    top = records[0]
    i18n_data = top.get("i18n", {}).get(language, top.get("i18n", {}).get("en", top))
    title = i18n_data.get("title", top["title"])
    summary = i18n_data.get("summary", top["summary"])
    guidance = i18n_data.get("guidance", top.get("guidance", "N/A"))

    if language == "hi":
        text = (
            f"ManakAI नॉलेज बेस के अनुसार, यह **{title}** ({top.get('standard_number', '')}) से संबंधित है।\n\n"
            f"{summary}\n\nमार्गदर्शन: {guidance}\n\n"
            f"(नोट: यह उत्तर सत्यापित स्रोत डेटा से प्रोटोटाइप जानकारी है।)"
        )
    elif language == "mr":
        text = (
            f"ManakAI नॉलेज बेसनुसार, हे **{title}** ({top.get('standard_number', '')}) शी संबंधित आहे.\n\n"
            f"{summary}\n\nमार्गदर्शन: {guidance}\n\n"
            f"(टीप: हे उत्तर सत्यापित स्रोत डेटावरून प्रोटोटाइप माहिती आहे.)"
        )
    else:  # en and fallback for other languages in demo mode
        text = (
            f"Based on the verified ManakAI knowledge base, this relates to **{title}**"
            f" ({top.get('standard_number', '')}).\n\n{summary}\n\nGuidance: {guidance}"
        )
    return text


def _llm_answer(query: str, records: List[Dict[str, Any]], language: str) -> Optional[str]:
    context_blocks = []
    for r in records:
        i18n_data = r.get("i18n", {}).get(language, r.get("i18n", {}).get("en", r))
        title = i18n_data.get("title", r["title"])
        summary = i18n_data.get("summary", r["summary"])
        guidance = i18n_data.get("guidance", r.get("guidance", "N/A"))

        context_blocks.append(
            f"Title: {title}\nStandard: {r.get('standard_number', '')}\nSummary: {summary}\nRequirements: {', '.join(r.get('requirements', []))}\n"
            f"Guidance: {guidance}\nSource: {r['source_name']} ({r['source_url']})"
        )
    context = "\n\n---\n\n".join(context_blocks)

    lang_name = LANG_NAMES.get(language, "English")
    system_prompt = (
        "You are ManakAI, a strictly grounded assistant for Indian Standards and BIS services. "
        "You must answer ONLY using the provided verified context records. "
        "If the provided context is insufficient, irrelevant to the user's question, or empty, "
        "you MUST reply with exactly 'NO VERIFIED MATCH' and nothing else. "
        "Never invent standards, requirements, documents, fees, URLs, timelines, licence/HUID status, alerts, or outcomes. "
        "Every successful answer must explicitly expose its verified source/evidence from the context (e.g., 'According to [Source Name]'). "
        "Keep answers concise (under 150 words), clear, and in simple language. "
        f"Respond in {lang_name}. Always make clear this is verified guidance from the provided context."
    )
    user_prompt = f"Context records:\n\n{context}\n\nUser question: {query}"

    try:
        return llm.generate(system_prompt, user_prompt)
    except Exception:
        return None


def answer_query(query: str, language: str = "en") -> Dict[str, Any]:
    language = language if language in LANG_NAMES else "en"

    # 1. BIS Scope Check
    if not _is_bis_scope(query):
        return {
            "answer": SCOPE_REJECT_TEXT.get(language, SCOPE_REJECT_TEXT["en"]),
            "matched_topic": None,
            "standard_number": None,
            "sources": [],
            "mode": "demo",
            "confidence": "none",
            "disclaimer": DISCLAIMERS[language],
        }

    # 2. Query Normalization & Intent
    detected_intent = intent.detect_intent(query)

    # 3. Local Verified KB Retrieval
    records = []
    if USE_HYBRID_RETRIEVAL:
        records = hybrid_retriever.hybrid_search(query, top_k=3, norm_context=None)
        if not records:
            is_ascii = all(ord(c) < 128 for c in query)
            if not is_ascii and llm.is_llm_configured():
                norm_context = llm.extract_query_context(query)
                if norm_context:
                    records = hybrid_retriever.hybrid_search(query, top_k=3, norm_context=norm_context)
    else:
        records = knowledge_base.search(query, top_k=3)

    # 4. Official BIS Source Discovery (Pipeline integration)
    # If necessary -> Official BIS Source Discovery -> Validation -> Extraction
    if not records:
        # We simulate the discovery pipeline failure securely as we cannot do live web scraping here.
        # This acts as the final Applicability Gate enforcing VERIFIED records only.
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
            if "NO VERIFIED MATCH" in text.upper():
                return {
                    "answer": NO_MATCH_TEXT[language],
                    "matched_topic": None,
                    "standard_number": None,
                    "sources": [],
                    "mode": "llm",
                    "confidence": "none",
                    "disclaimer": DISCLAIMERS[language],
                }
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
    language = language if language in LANG_NAMES else "en"

    if USE_HYBRID_RETRIEVAL:
        # Primary Path: Deterministic + Native Semantic (No LLM)
        records = hybrid_retriever.hybrid_search(description, top_k=3, norm_context=None)

        # Secondary Path: LLM Fallback
        if not records:
            is_ascii = all(ord(c) < 128 for c in description)
            if not is_ascii and llm.is_llm_configured():
                norm_context = llm.extract_query_context(description)
                if norm_context:
                    records = hybrid_retriever.hybrid_search(description, top_k=3, norm_context=norm_context)
    else:
        records = knowledge_base.search(description, top_k=3)

    if not records:
        return None
    top = records[0]
    i18n_data = top.get("i18n", {}).get(language, top.get("i18n", {}).get("en", top))

    return {
        "title": i18n_data.get("title", top["title"]),
        "standard_number": top["standard_number"],
        "topic": top["topic"],
        "summary": i18n_data.get("summary", top["summary"]),
        "guidance": i18n_data.get("guidance", top.get("guidance", "N/A")),
        "sources": [_record_to_source(r) for r in records],
        "confidence": "high",
    }
