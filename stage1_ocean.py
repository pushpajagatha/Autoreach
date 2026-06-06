import requests
import os
from dotenv import load_dotenv

load_dotenv()

def find_lookalike_companies(seed_domain, limit=10):
    print(f"\n[Stage 1] Finding lookalike companies for: {seed_domain}")
    
    api_key = os.getenv("OCEAN_API_KEY")
    print(f"  Using key starting with: {api_key[:10] if api_key else 'NONE'}")
    
    url = "https://api.ocean.io/v3/search/companies"
    headers = {
        "x-api-token": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "size": limit,
        "companiesFilters": {
            "lookalikeDomains": [seed_domain]
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
        response.raise_for_status()
        data = response.json()
        
        domains = []
        companies = data.get("companies", [])
        for company in companies:
            domain = company.get("company", {}).get("domain")
            if domain:
                domains.append(domain)
        
        if not domains:
            print("[Stage 1] No companies found")
            return []
        
        print(f"[Stage 1] Found {len(domains)} lookalike companies:")
        for d in domains:
            print(f"  → {d}")
        return domains
    
    except requests.exceptions.RequestException as e:
        print(f"[Stage 1] Error: {e}")
        return []