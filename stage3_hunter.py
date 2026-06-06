import requests
from config import HUNTER_API_KEY

def resolve_emails(contacts):
    print(f"\n[Stage 3] Resolving emails for {len(contacts)} contacts...")
    
    enriched_contacts = []
    
    for contact in contacts:
        # If email already found in Stage 2, skip Hunter
        if contact.get("email"):
            enriched_contacts.append(contact)
            print(f"  → {contact['first_name']} {contact['last_name']}: "
                  f"email already known ({contact['email']})")
            continue
        
        first_name = contact.get("first_name", "")
        last_name = contact.get("last_name", "")
        domain = contact.get("domain", "")
        
        if not domain or not first_name:
            print(f"  → Skipping — missing name or domain")
            continue
        
        url = "https://api.hunter.io/v2/email-finder"
        params = {
            "domain": domain,
            "first_name": first_name,
            "last_name": last_name,
            "api_key": HUNTER_API_KEY
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            email = data.get("data", {}).get("email", "")
            score = data.get("data", {}).get("score", 0)
            
            if email and score > 50:
                contact["email"] = email
                enriched_contacts.append(contact)
                print(f"  → {first_name} {last_name}: {email} "
                      f"(confidence: {score}%)")
            else:
                print(f"  → {first_name} {last_name}: no email found")
        
        except requests.exceptions.RequestException as e:
            print(f"  → {first_name} {last_name}: Error - {e}")
            continue
    
    print(f"[Stage 3] Resolved emails for {len(enriched_contacts)} contacts")
    return enriched_contacts