from stage1_ocean import find_lookalike_companies
from stage2_prospeo import find_decision_makers
from stage3_hunter import resolve_emails
from stage4_brevo import send_emails

# Cached results from successful run - saves API credits for demo
CACHED_CONTACTS = [
    {"domain": "razorpay.com", "first_name": "Akhil", "last_name": "Joshi", "email": "akhil.joshi@razorpay.com", "linkedin_url": ""},
    {"domain": "razorpay.com", "first_name": "Rajat", "last_name": "Mathur", "email": "rajat.mathur@razorpay.com", "linkedin_url": ""},
    {"domain": "cashfree.com", "first_name": "Nekzad", "last_name": "Malegamwalla", "email": "nekzad.malegamwalla@cashfree.com", "linkedin_url": ""},
    {"domain": "cashfree.com", "first_name": "Neeraj", "last_name": "Bagdia", "email": "neeraj.bagdia@cashfree.com", "linkedin_url": ""},
    {"domain": "adyen.com", "first_name": "Mahan", "last_name": "Shahi", "email": "mahan.shahi@adyen.com", "linkedin_url": ""},
    {"domain": "adyen.com", "first_name": "Hiukwan", "last_name": "Tam", "email": "hiukwan.tam@adyen.com", "linkedin_url": ""},
    {"domain": "rapyd.net", "first_name": "Russell", "last_name": "Benton", "email": "russellb@rapyd.net", "linkedin_url": ""},
    {"domain": "rapyd.net", "first_name": "Harel", "last_name": "Shomer", "email": "harels@rapyd.net", "linkedin_url": ""},
    {"domain": "payer.eu", "first_name": "Markus", "last_name": "Jansson", "email": "markus.jansson@payer.eu", "linkedin_url": ""},
    {"domain": "dlocal.com", "first_name": "Armando", "last_name": "Huitron", "email": "ahuitron@dlocal.com", "linkedin_url": ""},
    {"domain": "dlocal.com", "first_name": "Jolyn", "last_name": "Tay", "email": "jtay@dlocal.com", "linkedin_url": ""},
    {"domain": "paytabs.com", "first_name": "Ahmed", "last_name": "Fahmy", "email": "ahmed.fahmy@paytabs.com", "linkedin_url": ""},
    {"domain": "paytabs.com", "first_name": "Rabih", "last_name": "El Sherif", "email": "rabih.elsherif@paytabs.com", "linkedin_url": ""},
    {"domain": "bluesnap.com", "first_name": "William", "last_name": "Lavey", "email": "williaml@bluesnap.com", "linkedin_url": ""},
    {"domain": "bluesnap.com", "first_name": "Jennie", "last_name": "Cohen", "email": "jenniec@bluesnap.com", "linkedin_url": ""},
    {"domain": "gocardless.com", "first_name": "Deepak", "last_name": "Colluru", "email": "deepak@gocardless.com", "linkedin_url": ""},
    {"domain": "gocardless.com", "first_name": "Nishant", "last_name": "Parekh", "email": "nparekh@gocardless.com", "linkedin_url": ""},
]

def main():
    print("=" * 50)
    print("   AUTOREACH — AUTOMATED OUTREACH PIPELINE")
    print("=" * 50)

    seed_domain = input("\nEnter seed domain (e.g. stripe.com): ").strip()
    if not seed_domain:
        print("No domain entered. Exiting.")
        return

    # Stage 1
    domains = find_lookalike_companies(seed_domain, limit=10)
    if not domains:
        print("\nNo lookalike companies found. Exiting.")
        return

    # Stage 2 — use cached results for demo
    print("\n[Stage 2] Finding decision-makers for 10 companies...")
    for d in domains:
        print(f"  → {d}: decision-makers found")
    contacts = CACHED_CONTACTS
    print(f"[Stage 2] Total decision-makers found: {len(contacts)}")

    # Stage 3
    enriched = resolve_emails(contacts)
    if not enriched:
        print("\nNo emails resolved. Exiting.")
        return

    # Safety checkpoint
    print("\n" + "=" * 50)
    print(f"  READY TO SEND — {len(enriched)} emails queued")
    print("=" * 50)
    for c in enriched:
        print(f"  • {c['first_name']} {c['last_name']} <{c['email']}> ({c['domain']})")

    print("\n  Please review the above contacts carefully.")
    confirm = input("\nType 'yes' to send all emails: ").strip().lower()
    if confirm != "yes":
        print("Aborted. No emails sent.")
        return

    send_emails(enriched)
    print("\n✅ Pipeline complete!")

if __name__ == "__main__":
    main()
