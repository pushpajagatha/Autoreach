from stage1_ocean import find_lookalike_companies
from stage2_prospeo import find_decision_makers
from stage3_hunter import resolve_emails
from stage4_brevo import send_emails

def main():
    print("=" * 50)
    print("   AUTOREACH — AUTOMATED OUTREACH PIPELINE")
    print("=" * 50)
    
    # Single human input
    seed_domain = input("\nEnter seed domain (e.g. stripe.com): ").strip()
    if not seed_domain:
        print("No domain entered. Exiting.")
        return
    
    # Stage 1 — Find lookalike companies
    domains = find_lookalike_companies(seed_domain, limit=10)
    if not domains:
        print("\nNo lookalike companies found. Exiting.")
        return
    
    # Stage 2 — Find decision makers
    contacts = find_decision_makers(domains)
    if not contacts:
        print("\nNo decision-makers found. Exiting.")
        return
    
    # Stage 3 — Resolve emails
    enriched = resolve_emails(contacts)
    if not enriched:
        print("\nNo emails resolved. Exiting.")
        return
    
    # Safety checkpoint
    print("\n" + "=" * 50)
    print(f"  READY TO SEND — {len(enriched)} emails queued")
    print("=" * 50)
    for c in enriched:
        print(f"  • {c['first_name']} {c['last_name']} "
              f"<{c['email']}> ({c['domain']})")
    
    print("\n⚠️  Please review the above contacts carefully.")
    confirm = input("\nType 'yes' to send all emails: ").strip().lower()
    if confirm != "yes":
        print("Aborted. No emails sent.")
        return
    
    # Stage 4 — Send emails
    send_emails(enriched)
    print("\n✅ Pipeline complete!")

if __name__ == "__main__":
    main()