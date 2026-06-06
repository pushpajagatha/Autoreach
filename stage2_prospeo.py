import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

def reveal_email(person_id, api_key):
    url = "https://api.prospeo.io/enrich-person"
    headers = {
        "Content-Type": "application/json",
        "X-KEY": api_key
    }
    payload = {
        "data": {
            "person_id": person_id
        },
        "only_verified_email": True
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            person = data.get("person", {})
            email_data = person.get("email", {})
            if isinstance(email_data, dict):
                return email_data.get("email", "")
            elif isinstance(email_data, str):
                return email_data
    except Exception as e:
        print(f"    Enrich error: {e}")
    return ""

def find_decision_makers(domains):
    print(f"\n[Stage 2] Finding decision-makers for {len(domains)} companies...")
    
    all_contacts = []
    api_key = os.getenv("PROSPEO_API_KEY")
    
    for domain in domains:
        url = "https://api.prospeo.io/search-person"
        headers = {
            "Content-Type": "application/json",
            "X-KEY": api_key
        }
        payload = {
            "filters": {
                "company": {
                    "websites": {
                        "include": [domain]
                    }
                },
                "person_seniority": {
                    "include": ["C-Suite", "Vice President", "Director"]
                }
            },
            "page": 1
        }
        
        try:
            time.sleep(3)
            response = requests.post(url, json=payload, headers=headers)
            print(f"  → {domain}: Status {response.status_code}")
            
            if response.status_code != 200:
                print(f"  → Response: {response.text[:200]}")
                continue
                
            data = response.json()
            results = data.get("results", [])
            
            # Only take first 2 per domain to save credits
            for item in results[:2]:
                person = item.get("person", {})
                person_id = person.get("person_id", "")
                
                # Reveal real email
                email = ""
                if person_id:
                    print(f"    Enriching {person.get('first_name')}...")
                    email = reveal_email(person_id, api_key)
                    time.sleep(10)
                
                if email:
                    all_contacts.append({
                        "domain": domain,
                        "first_name": person.get("first_name", ""),
                        "last_name": person.get("last_name", ""),
                        "email": email,
                        "linkedin_url": person.get("linkedin_url", ""),
                        "person_id": person_id
                    })
                    print(f"    ✓ {person.get('first_name')}: {email}")
                else:
                    print(f"    ✗ {person.get('first_name')}: no email found")
            
            print(f"  → {domain}: done")
        
        except requests.exceptions.RequestException as e:
            print(f"  → {domain}: Error - {e}")
            continue
    
    print(f"[Stage 2] Total decision-makers found: {len(all_contacts)}")
    return all_contacts