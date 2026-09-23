import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['USE_HYBRID_RETRIEVAL'] = 'true'
from dotenv import load_dotenv
load_dotenv()

from app import rag

queries = [
    'laptop', 'laptops', 'notebook', 'notebooks',
    'laptop certification', 'laptop standard',
    'random unknown product', 'aircraft certification',
    'certification', 'testing', 'BIS'
]

print("Targeted Regression Tests:")
for q in queries:
    res = rag.find_standard_for_product(q)
    if res and res.get('sources'):
        print(f"{q} -> {res['sources'][0]['id']}")
    else:
        print(f"{q} -> NO VERIFIED MATCH")
