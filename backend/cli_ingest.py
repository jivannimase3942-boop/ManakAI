import argparse
from app.ingestion.fetcher import fetch_content
from app.ingestion.extractor import extract_metadata
from app.ingestion.normalizer import normalize_to_schema
from app.ingestion.validator import validate_and_store

def main():
    parser = argparse.ArgumentParser(description="ManakAI V2 Ingestion Pipeline Demo")
    parser.add_argument("--url", required=True, help="Official BIS URL to ingest (use mock.local/... for testing)")
    
    args = parser.parse_args()
    url = args.url
    
    print(f"[*] Starting ingestion for URL: {url}")
    
    try:
        print("[*] Fetching content...")
        html = fetch_content(url)
    except Exception as e:
        print(f"[!] Fetch failed: {e}")
        return
        
    print("[*] Extracting metadata...")
    extracted = extract_metadata(html, source_type="official")
    print(f"    -> Title: {extracted.get('title')}")
    print(f"    -> Standard Number: {extracted.get('standard_number')}")
    
    print("[*] Normalizing to schema...")
    normalized = normalize_to_schema(extracted, url)
    
    print("[*] Validating and storing...")
    success, msg, record = validate_and_store(normalized)
    
    if success:
        print(f"[+] Success! Record saved as PENDING.")
        print(f"    ID: {record.id}")
        print(f"    Status: {record.verification_status}")
    else:
        print(f"[-] Validation failed: {msg}")

if __name__ == "__main__":
    main()
