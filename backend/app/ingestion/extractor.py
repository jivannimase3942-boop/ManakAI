from bs4 import BeautifulSoup
from typing import Dict, Any

def extract_metadata(html_content: str, source_type: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html_content, 'html.parser')
    
    extracted = {
        "title": None,
        "standard_number": None,
        "summary": None,
        "requirements": []
    }
    
    # Very naive deterministic extraction for demo/test purposes
    title_tag = soup.find('h1', class_='standard-title')
    if title_tag:
        extracted["title"] = title_tag.get_text(strip=True)
        
    head_title = soup.find('title')
    if head_title and "IS" in head_title.text:
        parts = head_title.text.split(":")
        if len(parts) > 1:
            extracted["standard_number"] = parts[0].strip()
            if not extracted["title"]:
                extracted["title"] = parts[1].strip()
                
    summary_tag = soup.find('p', class_='summary')
    if summary_tag:
        extracted["summary"] = summary_tag.get_text(strip=True)
        
    req_div = soup.find('div', class_='requirements')
    if req_div:
        reqs = req_div.find_all('li')
        extracted["requirements"] = [li.get_text(strip=True) for li in reqs]
        
    return extracted
