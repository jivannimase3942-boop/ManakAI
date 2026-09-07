import sys
import logging
from app.ingestion.fetcher import fetch_content
from app.ingestion.extractors.laboratory import extract_laboratory_metadata
from app.ingestion.normalizer import normalize_to_schema
from app.ingestion.validator import validate_and_store

logging.basicConfig(level=logging.INFO)

url = "https://www.bis.gov.in/laboratorys/"

def main():
    print(f"[*] Fetching real source: {url}")
    try:
        html = fetch_content(url)
        print(f"[+] HTTP Status: Successfully fetched. Length: {len(html)}")
    except Exception as e:
        print(f"[-] Fetch failed: {e}")
        return
        
    print("[*] Extracting laboratory metadata...")
    extracted_records = extract_laboratory_metadata(html, url)
    
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
        print("[-] No records could be extracted.")

if __name__ == "__main__":
    main()
