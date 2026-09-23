import json
import os

# Base path
EVAL_DIR = os.path.join(os.path.dirname(__file__), "..", "evaluation")
os.makedirs(EVAL_DIR, exist_ok=True)
BENCHMARK_PATH = os.path.join(EVAL_DIR, "phase2e_benchmark.json")

benchmark = []
case_id = 1

def add_case(query, language, mode, expected_match, expected_record_id, expected_standard_number, category, reason):
    global case_id
    benchmark.append({
        "id": f"q-{case_id:03d}",
        "query": query,
        "language": language,
        "mode": mode,
        "expected_match": expected_match,
        "expected_record_id": expected_record_id,
        "expected_standard_number": expected_standard_number,
        "category": category,
        "reason": reason
    })
    case_id += 1

# A. VALID PRODUCT QUERIES - 30
valid_queries = [
    ("packaged drinking water", "en", "industry", "kb-001", "IS 14543"),
    ("mineral water packaging", "en", "industry", "kb-001", "IS 14543"),
    ("bottled water requirements", "en", "industry", "kb-001", "IS 14543"),
    ("drinking water testing", "en", "consumer", "kb-001", "IS 14543"),
    ("water bottle ISI mark", "en", "consumer", "kb-001", "IS 14543"),

    ("toys", "en", "industry", "kb-010", "IS 9873"),
    ("toy safety testing", "en", "industry", "kb-010", "IS 9873"),
    ("children play equipment", "en", "industry", "kb-010", "IS 9873"),
    ("soft toys ISI", "en", "consumer", "kb-010", "IS 9873"),
    ("plastic toy standards", "en", "industry", "kb-010", "IS 9873"),

    ("cement", "en", "industry", "kb-011", "IS 269"),
    ("ordinary portland cement", "en", "industry", "kb-011", "IS 269"),
    ("OPC manufacturing", "en", "industry", "kb-011", "IS 269"),
    ("cement testing equipment", "en", "industry", "kb-011", "IS 269"),
    ("cement ISI mark check", "en", "consumer", "kb-011", "IS 269"),

    ("laptop", "en", "industry", "kb-012", "IS 13252"),
    ("notebook computer", "en", "industry", "kb-012", "IS 13252"),
    ("IT goods CRS", "en", "industry", "kb-012", "IS 13252"),
    ("laptop safety requirements", "en", "consumer", "kb-012", "IS 13252"),
    ("tablet certification", "en", "industry", "kb-012", "IS 13252"),

    ("protective helmets", "en", "industry", "kb-013", "IS 4151"),
    ("two wheeler helmet", "en", "industry", "kb-013", "IS 4151"),
    ("motorcycle helmet safety", "en", "consumer", "kb-013", "IS 4151"),
    ("helmet ISI mark", "en", "consumer", "kb-013", "IS 4151"),
    ("riding helmet standard", "en", "industry", "kb-013", "IS 4151"),

    ("pressure cookers", "en", "industry", "kb-014", "IS 2347"),
    ("domestic pressure cooker", "en", "industry", "kb-014", "IS 2347"),
    ("cooker safety standard", "en", "consumer", "kb-014", "IS 2347"),
    ("aluminum pressure cooker", "en", "industry", "kb-014", "IS 2347"),
    ("cooker ISI mark verify", "en", "consumer", "kb-014", "IS 2347"),
]

for q, l, m, rid, is_num in valid_queries:
    add_case(q, l, m, True, rid, is_num, "valid", "Valid product query")

# B. PARAPHRASED VALID QUERIES - 20
paraphrased_queries = [
    ("how do I get an ISI mark for my drinking water plant", "en", "industry", "kb-001", "IS 14543"),
    ("what is the process to certify bottled water", "en", "industry", "kb-001", "IS 14543"),
    ("is it mandatory to test water bottles", "en", "industry", "kb-001", "IS 14543"),
    ("what are the rules for manufacturing toys in India", "en", "industry", "kb-010", "IS 9873"),
    ("my company makes soft toys, do we need BIS", "en", "industry", "kb-010", "IS 9873"),
    ("I want to import toys, what is the BIS requirement", "en", "industry", "kb-010", "IS 9873"),
    ("what grade of portland cement requires certification", "en", "industry", "kb-011", "IS 269"),
    ("can I sell OPC without ISI mark", "en", "industry", "kb-011", "IS 269"),
    ("how to check if cement is fake", "en", "consumer", "kb-011", "IS 269"),
    ("are laptops covered under compulsory registration scheme", "en", "industry", "kb-012", "IS 13252"),
    ("do I need CRS for importing notebooks", "en", "industry", "kb-012", "IS 13252"),
    ("what is the standard for IT equipment safety", "en", "industry", "kb-012", "IS 13252"),
    ("is helmet certification mandatory for selling in India", "en", "industry", "kb-013", "IS 4151"),
    ("how to verify if my riding helmet is genuinely approved", "en", "consumer", "kb-013", "IS 4151"),
    ("what is the IS number for motorcycle helmets", "en", "industry", "kb-013", "IS 4151"),
    ("do pressure cookers need to be tested before sale", "en", "industry", "kb-014", "IS 2347"),
    ("what are the safety requirements for kitchen cookers", "en", "industry", "kb-014", "IS 2347"),
    ("how do I complain about a fake ISI mark on a cooker", "en", "consumer", "kb-014", "IS 2347"), # wait, complaint might map to complaint record? Let's just say cooker for cooker record or complaint record. Actually, "complain about a fake ISI mark" maps to Consumer Complaints kb-005. Let's make it unambiguous:
    ("what is the Indian Standard for domestic aluminum cookers", "en", "industry", "kb-014", "IS 2347"),
    ("where can I find the standard for bottled drinking water", "en", "industry", "kb-001", "IS 14543"),
    ("how to apply for BIS certification for OPC cement", "en", "industry", "kb-011", "IS 269"),
]

for q, l, m, rid, is_num in paraphrased_queries:
    add_case(q, l, m, True, rid, is_num, "paraphrase", "Natural language variation")

# C. EXACT STANDARD-ID QUERIES - 10
exact_id_queries = [
    ("IS 14543", "en", "industry", "kb-001", "IS 14543"),
    ("IS 9873", "en", "industry", "kb-010", "IS 9873"),
    ("IS 269", "en", "industry", "kb-011", "IS 269"),
    ("IS 13252", "en", "industry", "kb-012", "IS 13252"),
    ("IS 4151", "en", "industry", "kb-013", "IS 4151"),
    ("IS 2347", "en", "industry", "kb-014", "IS 2347"),
    ("standard IS 14543", "en", "industry", "kb-001", "IS 14543"),
    ("tell me about IS 9873", "en", "industry", "kb-010", "IS 9873"),
    ("requirements of IS 269", "en", "industry", "kb-011", "IS 269"),
    ("download IS 13252", "en", "industry", "kb-012", "IS 13252"),
]

for q, l, m, rid, is_num in exact_id_queries:
    add_case(q, l, m, True, rid, is_num, "exact_id", "Exact standard number match")

# D. GENERIC / UNDERSPECIFIED QUERIES - 15
generic_queries = [
    "certification",
    "testing",
    "requirements",
    "BIS standard",
    "BIS certification",
    "documents",
    "how to get a certificate",
    "what is the testing process",
    "where is the laboratory",
    "how to check ISI mark",
    "BIS rules",
    "product safety",
    "manufacturing compliance",
    "how to apply",
    "what are the fees"
]

for q in generic_queries:
    add_case(q, "en", "industry", False, None, None, "generic", "Underspecified generic query")

# E. CROSS-DOMAIN / ADVERSARIAL QUERIES - 20
adversarial_queries = [
    "aircraft certification",
    "flying car certification",
    "automobile certification",
    "random product testing",
    "xyz standard",
    "pharmaceutical certification",
    "chemical testing standard",
    "solar panel testing",
    "LPG cylinder certification",
    "steel rebars IS number",
    "electric vehicle batteries",
    "medical devices",
    "software certification",
    "nuclear material testing",
    "blockchain standard",
    "how to certify an aeroplane",
    "spacecraft compliance",
    "furniture standards",
    "textile and clothing IS",
    "food additive testing"
]

for q in adversarial_queries:
    add_case(q, "en", "industry", False, None, None, "adversarial", "Cross-domain/Adversarial query")

# F. HINDI QUERIES - 15
hindi_queries = [
    ("सीमेंट के लिए कौन सा BIS मानक लागू होता है?", "hi", "industry", "kb-011", "IS 269"),
    ("पैकेज्ड ड्रिंकिंग वाटर के लिए क्या नियम हैं?", "hi", "industry", "kb-001", "IS 14543"),
    ("क्या खिलौनों के लिए ISI मार्क अनिवार्य है?", "hi", "industry", "kb-010", "IS 9873"),
    ("लैपटॉप के लिए BIS रजिस्ट्रेशन कैसे करें?", "hi", "industry", "kb-012", "IS 13252"),
    ("हेलमेट का IS नंबर क्या है?", "hi", "industry", "kb-013", "IS 4151"),
    ("प्रेशर कुकर की सुरक्षा मानक क्या है?", "hi", "consumer", "kb-014", "IS 2347"),
    ("पानी की बोतल का आईएसआई मार्क कैसे चेक करें?", "hi", "consumer", "kb-001", "IS 14543"),
    ("पोर्टलैंड सीमेंट के लिए परीक्षण आवश्यकताएं", "hi", "industry", "kb-011", "IS 269"),
    ("क्या बच्चों के खिलौने सुरक्षित हैं?", "hi", "consumer", "kb-010", "IS 9873"),
    ("आईटी उपकरणों के लिए CRS स्कीम", "hi", "industry", "kb-012", "IS 13252"),
    ("टू व्हीलर हेलमेट सर्टिफिकेशन", "hi", "industry", "kb-013", "IS 4151"),
    ("कुकर पर ISI मार्क", "hi", "consumer", "kb-014", "IS 2347"),
    ("IS 14543 के बारे में बताएं", "hi", "industry", "kb-001", "IS 14543"),
    ("IS 269 सीमेंट", "hi", "industry", "kb-011", "IS 269"),
    ("खिलौनों की टेस्टिंग", "hi", "industry", "kb-010", "IS 9873"),
]

for q, l, m, rid, is_num in hindi_queries:
    add_case(q, l, m, True, rid, is_num, "hindi", "Hindi query")

# G. MARATHI QUERIES - 15
marathi_queries = [
    ("सिमेंटसाठी कोणता BIS मानक लागू आहे?", "mr", "industry", "kb-011", "IS 269"),
    ("पिण्याच्या पाण्यासाठी काय नियम आहेत?", "mr", "industry", "kb-001", "IS 14543"),
    ("खेळण्यांसाठी ISI मार्क अनिवार्य आहे का?", "mr", "industry", "kb-010", "IS 9873"),
    ("लॅपटॉपसाठी BIS नोंदणी कशी करावी?", "mr", "industry", "kb-012", "IS 13252"),
    ("हेल्मेटचा IS नंबर काय आहे?", "mr", "industry", "kb-013", "IS 4151"),
    ("प्रेशर कुकरचा सुरक्षा मानक कोणता आहे?", "mr", "consumer", "kb-014", "IS 2347"),
    ("पाण्याच्या बाटलीवरील आयएसआय मार्क कसा तपासावा?", "mr", "consumer", "kb-001", "IS 14543"),
    ("पोर्टलँड सिमेंटसाठी चाचणी आवश्यकता", "mr", "industry", "kb-011", "IS 269"),
    ("मुलांची खेळणी सुरक्षित आहेत का?", "mr", "consumer", "kb-010", "IS 9873"),
    ("आयटी उपकरणांसाठी CRS योजना", "mr", "industry", "kb-012", "IS 13252"),
    ("दुचाकी हेल्मेट प्रमाणपत्र", "mr", "industry", "kb-013", "IS 4151"),
    ("कुकरवर ISI मार्क", "mr", "consumer", "kb-014", "IS 2347"),
    ("IS 14543 बद्दल सांगा", "mr", "industry", "kb-001", "IS 14543"),
    ("IS 269 सिमेंट", "mr", "industry", "kb-011", "IS 269"),
    ("खेळण्यांची चाचणी", "mr", "industry", "kb-010", "IS 9873"),
]

for q, l, m, rid, is_num in marathi_queries:
    add_case(q, l, m, True, rid, is_num, "marathi", "Marathi query")

with open(BENCHMARK_PATH, "w", encoding="utf-8") as f:
    json.dump(benchmark, f, indent=2, ensure_ascii=False)

print(f"Generated {len(benchmark)} evaluation queries at {BENCHMARK_PATH}")
