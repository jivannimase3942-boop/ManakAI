import logging
from bs4 import BeautifulSoup
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def extract_compulsory_products(html_content: str, source_url: str) -> List[Dict[str, Any]]:
    """
    Extracts products from the BIS Compulsory Certification tables.
    Returns a list of extracted dictionaries ready for normalization.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    
    if not tables:
        logger.warning("No tables found in the compulsory certification HTML.")
        return []

    extracted_records = []
    
    for table in tables:
        rows = table.find_all('tr')
        if not rows:
            continue
            
        # Detect headers
        headers = [th.get_text(strip=True).lower() for th in rows[0].find_all(['th', 'td'])]
        
        # We need at least product and standard columns to be useful
        product_idx = -1
        standard_idx = -1
        
        for i, h in enumerate(headers):
            if 'product' in h or 'item' in h or 'article' in h:
                product_idx = i
            elif 'standard' in h or 'is no' in h or 'is/' in h:
                standard_idx = i
                
        if product_idx == -1 or standard_idx == -1:
            # Maybe the table doesn't have a clear header row. Let's fallback to checking row content.
            # But the requirement says: "If the expected table structure is missing, return no records and log a clear extraction warning instead of fabricating data."
            logger.warning(f"Skipping table: could not identify Product and Standard columns. Headers found: {headers}")
            continue
            
        for row in rows[1:]:
            cols = row.find_all(['td', 'th'])
            if len(cols) <= max(product_idx, standard_idx):
                continue
                
            product_name = cols[product_idx].get_text(strip=True)
            standard_num = cols[standard_idx].get_text(strip=True)
            
            if not product_name or not standard_num:
                continue
                
            extracted_records.append({
                "title": product_name,
                "standard_number": standard_num,
                "scheme": "Scheme-I (ISI Mark)", # Typically true for compulsory, but leaving safe default
                "applicability": "Mandatory Certification Required",
                "source_url": source_url,
                "source_name": "BIS Compulsory Certification List",
                "source_type": "official"
            })

    return extracted_records
