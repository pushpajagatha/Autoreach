# AutoReach — Automated Outreach Pipeline

A CLI tool that automates cold outreach end to end.
One domain in → emails sent. Zero manual steps.

## Pipeline
1. Ocean.io → Find lookalike companies
2. Prospeo → Find decision-makers
3. Hunter.io → Resolve work emails
4. Brevo → Send personalized emails

## Setup
1. Clone the repo
2. Install dependencies:
   pip install requests python-dotenv
3. Create .env file with your API keys:
   OCEAN_API_KEY=your_key
   PROSPEO_API_KEY=your_key
   HUNTER_API_KEY=your_key
   BREVO_API_KEY=your_key
4. Run:
   python main.py

## Safety
Pipeline shows a summary of all contacts
before sending any emails — requires manual
confirmation to proceed.