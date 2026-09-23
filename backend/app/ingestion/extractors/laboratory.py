import logging
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def extract_laboratory_metadata(html_content: str, source_url: str) -> List[Dict[str, Any]]:
    """
    Extracts static laboratory information from the BIS Laboratory page.
    This safely targets only explicitly present static text and links.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check for LIMS / SPA structures which we should skip
    if soup.find('app-root'):
        logger.warning(f"Source at {source_url} appears to be an SPA (LIMS). Aborting extraction to prevent dynamic scraping.")
        return []

    # Find the main content area
    main_content = soup.find('main') or soup.find('div', class_='entry-content') or soup.find('article') or soup.find('body')
    
    if not main_content:
        logger.warning("No main content found for laboratory information.")
        return []

    extracted_records = []
    
    # We will look for static paragraphs or headings that describe laboratory services
    # For example, "Laboratory Recognition Scheme" or "Testing Facilities"
    keywords = ["laboratory recognition scheme", "testing facilit", "lims", "recognized lab"]
    
    # We can extract paragraphs containing these keywords as guidance
    paras = main_content.find_all(['p', 'h1', 'h2', 'h3', 'li'])
    
    collected_text = []
    for p in paras:
        text = p.get_text(strip=True)
        if len(text) > 20 and any(k in text.lower() for k in keywords):
            collected_text.append(text)
            
    # Also find important official links (e.g., links to LIMS portal)
    links = main_content.find_all('a')
    lims_links = []
    for a in links:
        href = a.get('href', '')
        text = a.get_text(strip=True)
        if 'lims.bis.gov.in' in href or 'laboratory' in text.lower():
            lims_links.append(f"{text}: {href}")

    if not collected_text and not lims_links:
        logger.warning("No static laboratory guidance found on the page.")
        return []

    # Combine into a single descriptive record representing the static information found on the page
    description = "\\n".join(collected_text[:5]) # keep it bounded
    if lims_links:
        description += "\\n\\nImportant Links:\\n" + "\\n".join(lims_links[:5])

    extracted_records.append({
        "title": "BIS Laboratory & Testing Information",
        "standard_number": None, # explicitly null for general guidance
        "scheme": "Laboratory Recognition Scheme / LIMS",
        "applicability": description[:500] + ("..." if len(description) > 500 else ""),
        "source_url": source_url,
        "source_name": "BIS Official Laboratory Directory Page",
        "source_type": "official"
    })

    return extracted_records
