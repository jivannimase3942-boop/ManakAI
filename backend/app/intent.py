import re

def detect_intent(query: str) -> str:
    """
    Deterministic rule-based intent engine.
    Detects the primary intent from a user's query.
    """
    q = query.lower()

    if re.search(r'\b(document|documents|form|checklist|paperwork)\b', q):
        return "DOCUMENTS"

    if re.search(r'\b(test|testing|laboratory|lab|recognised lab)\b', q):
        return "TESTING"

    if re.search(r'\b(complain|complaint|fake|grievance)\b', q):
        return "COMPLAINT"

    if re.search(r'\b(verify huid|verify license|verify licence|verify|check)\b', q):
        return "CONSUMER_VERIFICATION"

    if re.search(r'\b(hallmark|hallmarking|huid|gold|silver)\b', q):
        return "HALLMARKING"

    if re.search(r'\b(license|licence|licensing)\b', q):
        return "LICENSING"

    if re.search(r'\b(certification|certificate|isi mark|get mark)\b', q):
        return "CERTIFICATION"

    if re.search(r'\b(scheme|which scheme|what scheme|crs)\b', q):
        return "SCHEME_IDENTIFICATION"

    if re.search(r'\b(requirement|requirements|need|make)\b', q):
        return "REQUIREMENTS"

    if re.search(r'\b(standard|which standard|applies|is number)\b', q):
        return "STANDARD_IDENTIFICATION"

    if re.search(r'\b(what is|explain|general)\b', q):
        return "GENERAL_INFORMATION"

    return "UNKNOWN"
