import os
import sys
from dotenv import load_dotenv

# Ensure backend is in PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from app import semantic_retriever
from app import knowledge_base

def diagnose_semantic():
    cases = [
        # Hindi
        ("सीमेंट के लिए कौन सा BIS मानक लागू है?", "hi"),
        ("खिलौनों के लिए BIS मानक क्या है?", "hi"),
        ("पैकेज्ड ड्रिंकिंग वाटर का मानक क्या है?", "hi"),
        ("पोर्टलैंड सीमेंट के लिए परीक्षण आवश्यकताएँ", "hi"),
        # Marathi
        ("सिमेंटसाठी कोणता BIS मानक लागू आहे?", "mr"),
        ("खेळण्यांसाठी BIS मानक काय आहे?", "mr"),
        ("पॅकेज्ड ड्रिंकिंग वॉटरसाठी कोणता मानक आहे?", "mr"),
        ("पोर्टलँड सिमेंटसाठी चाचणी आवश्यकता", "mr"),
        # Hindi Unsupported / Generic
        ("विमान प्रमाणन", "hi"), # aircraft certification
        ("प्रयोगशाला कहाँ है", "hi"), # where is the laboratory
        # Marathi Unsupported / Generic
        ("प्रमाणन", "mr"), # certification
    ]

    print("Diagnosing Multilingual Semantic Retrieval (Direct Embeddings)")
    print("=" * 60)

    kb_records = {r["id"]: r for r in knowledge_base.all_records()}

    for query, lang in cases:
        print(f"\nQuery: {query}")
        print(f"Language: {lang}")

        try:
            candidates = semantic_retriever.get_semantic_candidates(query, top_k=5)
            print("Top 5 Semantic Candidates:")
            for rank, cand in enumerate(candidates, 1):
                rec_id = cand["record_id"]
                sim = cand["similarity"]
                record = kb_records.get(rec_id, {})
                title = record.get("title", "Unknown")
                std_num = record.get("standard_number", "None")
                print(f"  {rank}. ID: {rec_id} | Title: {title} | Std: {std_num} | Sim: {sim:.4f}")
        except Exception as e:
            print(f"Error retrieving candidates: {e}")

if __name__ == "__main__":
    diagnose_semantic()
