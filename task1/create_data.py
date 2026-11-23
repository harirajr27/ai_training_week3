import pandas as pd

data = [
    # Billing (16 rows)
    {"text": "Charged twice for my monthly subscription", "category": "Billing"},
    {"text": "Need an invoice for last month payment", "category": "billing"},
    {"text": "Refund not received after cancelling plan", "category": "BILLING"},
    {"text": "Update my credit card details on file", "category": "Billing"},
    {"text": "Why was I billed an extra $20 fee?", "category": "Billing"},
    {"text": "Promo code did not apply at checkout", "category": "billing"},
    {"text": "Download tax receipt for annual renewal", "category": "Billing"},
    {"text": "Payment failed with error code 402", "category": "BILLING"},
    {"text": "Switch from monthly to yearly billing cycle", "category": "Billing"},
    {"text": "Cancel auto-renewal for my team plan", "category": "Billing"},
    {"text": "Overcharged on my latest statement", "category": "billing"},
    {"text": "Need a VAT invoice for company accounting", "category": "Billing"},
    {"text": "Card declined even though funds are available", "category": "Billing"},
    {"text": "Charged twice for my monthly subscription", "category": "Billing"},  # Duplicate 1
    {"text": "Need an invoice for last month payment", "category": "billing"},     # Duplicate 2
    {"text": "Refund requested for accidental upgrade", "category": None},          # Missing 1

    # Technical (15 rows)
    {"text": "App crashes immediately when opening dashboard", "category": "Technical"},
    {"text": "API returns 500 internal server error", "category": "technical"},
    {"text": "Cannot export report to CSV format", "category": "TECHNICAL"},
    {"text": "Website loading very slowly on Chrome", "category": "Technical"},
    {"text": "Two-factor authentication SMS code not arriving", "category": "Technical"},
    {"text": "Webhook integration stopped triggering events", "category": "technical"},
    {"text": "Dark mode toggle is broken on mobile app", "category": "Technical"},
    {"text": "File upload fails for PDFs larger than 5MB", "category": "TECHNICAL"},
    {"text": "Search bar freezes when typing special characters", "category": "Technical"},
    {"text": "Database sync stuck at 99 percent", "category": "Technical"},
    {"text": "Error 404 when clicking notification link", "category": "technical"},
    {"text": "App crashes immediately when opening dashboard", "category": "Technical"}, # Duplicate 3
    {"text": "API returns 500 internal server error", "category": "technical"},         # Duplicate 4
    {"text": None, "category": "Technical"},                                           # Missing 2
    {"text": "Dashboard widgets fail to load metrics", "category": None},              # Missing 3

    # Account (15 rows)
    {"text": "Forgot my password and reset link expired", "category": "Account"},
    {"text": "How do I change my registered email address?", "category": "account"},
    {"text": "Account locked after too many login attempts", "category": "ACCOUNT"},
    {"text": "Add three new team members to my workspace", "category": "Account"},
    {"text": "Delete my account and all personal data", "category": "Account"},
    {"text": "Cannot log in using Google SSO", "category": "account"},
    {"text": "Change admin permissions for a user", "category": "Account"},
    {"text": "Update company profile name and logo", "category": "ACCOUNT"},
    {"text": "Deactivate former employee access", "category": "Account"},
    {"text": "Username already taken error during setup", "category": "Account"},
    {"text": "Merge two duplicate user profiles", "category": "account"},
    {"text": "Forgot my password and reset link expired", "category": "Account"}, # Duplicate 5
    {"text": None, "category": "Account"},                                       # Missing 4
    {"text": "Reset security questions for my login", "category": None},           # Missing 5
    {"text": None, "category": None}                                             # Missing 6
]

df = pd.DataFrame(data)
df.to_csv("tickets_raw.csv", index=False)
print("Created tickets_raw.csv with", len(df), "rows.")
