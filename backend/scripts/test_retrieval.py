from dotenv import load_dotenv
load_dotenv()
from app.rag import answer_query

queries = [
    'packaged drinking water',
    'cement',
    'toys',
    'protective helmets',
    'pressure cookers',
    'LPG cylinders',
    'steel rebars',
    'laptop',
    'certification',
    'testing',
    'aircraft certification',
    'random unknown product'
]

for q in queries:
    res = answer_query(q)
    print(f"Query: {q}")
    if res and res.get("matched_topic"):
        print(f"Match: {res.get('matched_topic')}")
        print(f"Confidence: {res.get('confidence', 'none')}")
    else:
        print("Match: No Match")
    print("---")
