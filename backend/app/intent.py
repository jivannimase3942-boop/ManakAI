import re

def detect_intent(query: str) -> str:
    """
    Deterministic rule-based intent engine.
    Detects the primary intent from a user's query.
    """
    q = query.lower()

    if re.search(r'\b(manufacture|msme|roadmap|what do i need to check for bis compliance|what bis compliance should i check|copilot)\b', q) or re.search(r'(मैं निर्माण करता हूँ|MSME|रोडमैप)', q, re.IGNORECASE):
        return "MSME_COPILOT"

    if re.search(r'\b(document|documents|form|checklist|paperwork)\b', q):
        return "DOCUMENTS"

    if re.search(r'\b(test|tests|tested|testing|laboratory|lab|recognised lab)\b', q) or re.search(r'(परीक्षण|प्रयोगशाला|जांच|चाचणी|प्रयोगशाळा)', q):
        return "TESTING"

    if re.search(r'\b(complain|complaint|fake|grievance)\b', q) or re.search(r'(शिकायत|तक्रार)', q):
        return "COMPLAINT"

    if re.search(r'\b(verify huid|verify license|verify licence|verify|check)\b', q):
        return "CONSUMER_VERIFICATION"

    if re.search(r'\b(hallmark|hallmarking|huid|gold|silver)\b', q) or re.search(r'(हॉलमार्क)', q):
        return "HALLMARKING"

    if re.search(r'\b(license|licence|licensing)\b', q) or re.search(r'(लाइसेंस|परवाना)', q):
        return "LICENSING"

    if re.search(r'\b(certification|certificate|isi mark|get mark)\b', q) or re.search(r'(प्रमाणन|प्रमाणपत्र)', q):
        return "CERTIFICATION"

    if re.search(r'\b(scheme|which scheme|what scheme|crs)\b', q) or re.search(r'(योजना|स्कीम)', q):
        return "SCHEME"

    if re.search(r'\b(requirement|requirements|need|make)\b', q) or re.search(r'(आवश्यकता|आवश्यक)', q):
        return "REQUIREMENTS"

    if re.search(r'\b(standard|which standard|applies|is number)\b', q) or re.search(r'(मानक|मानक क्रमांक|आयएस क्रमांक)', q):
        return "STANDARD_DISCOVERY"

    if re.search(r'\b(what is|explain|general)\b', q):
        return "GENERAL_BIS_GUIDANCE"

    return "UNKNOWN"
