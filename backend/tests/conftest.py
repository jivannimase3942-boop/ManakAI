import pytest
import os
import numpy as np

# A deterministic mapping for testing semantic relations without live Gemini calls
MOCK_ROUTING = {
    "drinking water": "kb-001",
    "cement": "kb-011",
    "सिमेंटसाठी": "kb-011",
    "खिलौनों": "kb-010",
    "प्रयोगशाला": "kb-004",
    "लॅबमध्ये": "kb-004",
    "mobile": "kb-019",
    "smartphone": "kb-019",
    "मोबाइल": "kb-019",
    "मोबाईल": "kb-019",
    "power bank": "kb-020",
    "पावर बैंक": "kb-020",
    "पॉवर बँक": "kb-020",
    "led": "kb-021",
    "एलईडी": "kb-021",
    "pvc": "kb-022",
    "पीवीसी": "kb-022",
    "पीव्हीसी": "kb-022",
    "plywood": "kb-023",
    "प्लायवुड": "kb-023",
    "footwear": "kb-024",
    "सेफ्टी": "kb-024",
    "सुरक्षा पादत्राणे": "kb-024",
    "ac": "kb-025",
    "एसी": "kb-025",
    "वातानुकूलक": "kb-025",
    "fan": "kb-026",
    "फैन": "kb-026",
    "फॅन": "kb-026",
    "pressure cooker": "kb-014",
    "14543": "kb-001",
    "13614": "kb-030",
    "269": "kb-011",
    "lab": "kb-004",
    "testing": "kb-004",
    "random": "kb-999",
    "flying": "kb-999",
    "aircraft": "kb-999",
    "apply": "kb-003",
}

# Cache for loaded real KB vectors to return as mock embeddings
_test_kb_vectors = None
_test_kb_ids = None

import re

def is_word_in_text(word, text):
    if all(ord(c) < 128 for c in word):
        return bool(re.search(r'\b' + re.escape(word) + r'\b', text))
    return word in text

def get_target_id(text):
    t = text.lower()
    for k, v in MOCK_ROUTING.items():
        if is_word_in_text(k, t):
            return v
    # If no product matches, return a zero vector indicator for negative queries
    return "ZERO_VECTOR"

def mock_get_embedding(text: str) -> np.ndarray:
    global _test_kb_vectors, _test_kb_ids
    if _test_kb_vectors is None:
        try:
            cache_path = os.path.join(os.path.dirname(__file__), '../../data/embeddings_cache.npz')
            data = np.load(cache_path, allow_pickle=True)
            _test_kb_vectors = data['embeddings']
            _test_kb_ids = data['record_ids']
        except Exception as e:
            return np.zeros(768, dtype=np.float32)

    target = get_target_id(text)
    if target == "ZERO_VECTOR":
        return np.zeros(768, dtype=np.float32)

    # Find index of target
    try:
        idx = list(_test_kb_ids).index(target)
        return _test_kb_vectors[idx]
    except ValueError:
        return np.zeros(768, dtype=np.float32)

def mock_extract_query_context(query: str, language: str) -> dict:
    t = query.lower()
    entity = ""
    if "toys" in t or " -  O \"< ," in t or "\u0916\u093f\u0932\u094c\u0928\u094b\u0902" in t: entity = "toys"
    elif "cement" in t or " ,  r؅ , Y , _ ?" in t: entity = "cement"
    elif "mobile" in t or "smartphone" in t or "\u092e\u094b\u092c\u093e\u0907\u0932" in t or "\u092e\u094b\u092c\u093e\u0908\u0932" in t or " r<  _ ؅ " in t or " r<  _ ^ " in t: entity = "mobile phone"
    elif "power bank" in t or "\u092a\u093e\u0935\u0930 \u092c\u0948\u0902\u0915" in t or "\u092a\u0949\u0935\u0930 \u092c\u0901\u0915" in t or "  _    ^ ,  " in t or " %     ?  " in t: entity = "power bank"
    elif "led" in t or "\u090f\u0932\u0908\u0921\u0940" in t or " ?  ^ ?" in t: entity = "LED bulb"
    elif "pvc" in t or "\u092a\u0940\u0935\u0940\u0938\u0940" in t or "\u092a\u0940\u0935\u094d\u0939\u0940\u0938\u0940" in t or " ? 慝? ,?" in t or " ? 慝? 1? ,?" in t: entity = "PVC pipe"
    elif "plywood" in t or "\u092a\u094d\u0932\u093e\u092f\u0935\u0941\u0921" in t or " ?  _ _ 慝? " in t: entity = "plywood"
    elif "footwear" in t or "\u0938\u0947\u092b\u094d\u091f\u0940" in t or "\u0938\u0941\u0930\u0915\u094d\u0937\u093e" in t or " ,؅ ? Y?" in t or " ,?   ?  _   _ ݅  ?  _ " in t: entity = "safety footwear"
    elif "ac" in t or "split ac" in t or "\u090f\u0938\u0940" in t or "\u0935\u093e\u0924\u093e\u0928\u0941\u0915\u0942\u0932\u0915" in t or " ? ,?" in t or "  _   _ \"?  ,   " in t: entity = "split AC"
    elif "fan" in t or "\u092b\u0948\u0928" in t or "\u092b\u0945\u0928" in t or " ^ \"" in t or " . \"" in t: entity = "ceiling fan"
    elif "pressure cooker" in t: entity = "pressure cooker"

    if entity:
        return {"product_entity": entity, "is_generic_query": False, "normalized_query": t, "confidence": 1.0}

    if "प्रयोगशाला" in t: return {"product_entity": "", "service_entity": "testing", "is_generic_query": True, "normalized_query": "where is the laboratory?", "confidence": 1.0}
    if "लॅबमध्ये" in t: return {"product_entity": "", "service_entity": "testing", "is_generic_query": True, "normalized_query": "how to go to the lab?", "confidence": 1.0}
    if "random" in t or "flying" in t or "aircraft" in t or "\u0930\u0901\u0921\u092e" in t or "\u0909\u0921\u093c\u0928\u0947" in t or "\u0909\u0921\u0923\u093e\u0930\u0940" in t or "\u0909\u0921\u0928\u093e\u0930\u0940" in t or "\u0935\u093f\u092e\u093e\u0928" in t or "viman" in t:
        return {"product_entity": "aircraft", "service_entity": "", "is_generic_query": False, "normalized_query": t, "confidence": 1.0}

    return {"product_entity": "", "is_generic_query": False, "normalized_query": t, "confidence": 1.0}

def mock_generate(prompt: str) -> str:
    # A dummy localized string to satisfy answer generation testing
    return "Mock localized BIS response."

@pytest.fixture(autouse=True)
def patch_external_gemini_calls(monkeypatch):
    import app.semantic_retriever
    import app.llm
    import app.rag
    import app.decision
    import app.embeddings

    original_load_cache = app.embeddings.EmbeddingCacheManager.load_cache

    def mock_load_cache(self):
        import numpy as np
        import os
        if "pytest" not in str(self.cache_path) and "Temp" not in str(self.cache_path) and "tmp" not in str(self.cache_path):
            cache_path = os.path.join(os.path.dirname(__file__), '../../data/embeddings_cache.npz')
            try:
                data = np.load(cache_path, allow_pickle=True)
                return data['embeddings'], data['record_ids']
            except Exception:
                return None, None
        return original_load_cache(self)

    monkeypatch.setattr(app.embeddings.EmbeddingCacheManager, "load_cache", mock_load_cache)

    # Mock embedding generation boundary where it's used
    monkeypatch.setattr(app.semantic_retriever, "get_embedding", mock_get_embedding)

    # extract_query_context only takes 1 argument `query`, my mock takes 2 (`query` and `language`). I need to fix the mock definition too!
    def _mock_extract_wrapper(query: str):
        return mock_extract_query_context(query, "en") # language is omitted in real signature

    monkeypatch.setattr(app.llm, "extract_query_context", _mock_extract_wrapper)
    monkeypatch.setattr(app.llm, "generate", mock_generate)
