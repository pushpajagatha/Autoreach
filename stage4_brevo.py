import requests
from config import BREVO_API_KEY

SENDER_NAME = "Pushpa Kumari"
SENDER_EMAIL = "pushpa@pushpa.space"

def build_email_body(first_name, company_domain):
    return f"""Hi {first_name},

I came across {company_domain} and was genuinely impressed by what your team is building.

I'm reaching out because I believe there's a strong synergy between what you're doing and how we can help you scale faster. Many companies in your space have used our approach to streamline their operations and drive measurable growth.

Would you be open to a quick 15-minute call this week? I'd love to share a few specific ideas that could be relevant to {company_domain}.

Looking forward to connecting!

Best regards,
Pushpa Kumari
AutoReach
pushpa@pushpa.space
"""

def send_emails(contacts):
    print(f"\n[Stage 4] Sending emails to {len(contacts)} contacts...")
    
    sent = 0
    failed = 0
    
    for contact in contacts:
        email = contact.get("email", "")
        first_name = contact.get("first_name", "there")
        last_name = contact.get("last_name", "")
        domain = contact.get("domain", "your company")
        
        if not email:
            print(f"  → Skipping {first_name} — no email")
            continue
        
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "sender": {
                "name": SENDER_NAME,
                "email": SENDER_EMAIL
            },
            "to": [{
                "email": email,
                "name": f"{first_name} {last_name}"
            }],
            "subject": f"Quick idea for {domain}",
            "textContent": build_email_body(first_name, domain)
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"  ✓ Sent to {first_name} {last_name} ({email})")
            sent += 1
        
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Failed to send to {email}: {e}")
            failed += 1
    
    print(f"\n[Stage 4] Done — {sent} sent, {failed} failed")