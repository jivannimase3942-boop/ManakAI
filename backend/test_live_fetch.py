import sys
import logging
from app.ingestion.fetcher import fetch_content
from app.ingestion.extractors.compulsory import extract_compulsory_products
from app.ingestion.normalizer import normalize_to_schema
from app.ingestion.validator import validate_and_store

logging.basicConfig(level=logging.INFO)

url = "https://www.bis.gov.in/product-certification/products-under-compulsory-certification/"

def main():
    print(f"[*] Fetching real source: {url}")
    try:
        html = fetch_content(url)
    except Exception as e:
        print(f"[-] Fetch failed: {e}")
        return
        
    print("[*] Extracting compulsory products...")
    extracted_records = extract_compulsory_products(html, url)
    
    print(f"[*] Extracted {len(extracted_records)} records.")
    
    if extracted_records:
        success_count = 0
        for ext in extracted_records:
            normalized = normalize_to_schema(ext, url)
            success, msg, rec = validate_and_store(normalized)
            if success:
                success_count += 1
                
        print(f"[+] Successfully validated and inserted {success_count} records as PENDING.")
    else:
        print("[-] No records could be extracted. The table structure may have changed or the data is in PDFs.")

if __name__ == "__main__":
    main()
