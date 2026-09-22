from app.database.database import get_all_leads

leads = get_all_leads()

for lead in leads:
    print("\n-----------------------------")
    print("Lead ID:", lead["id"])
    print("Name:", lead["name"])
    print("Phone:", lead["phone"])
    print("Location:", lead["location"])
    print("BHK:", lead["bhk"])
    print("Budget:", lead["budget_max"])
    print("Timeline:", lead["timeline"])
    print("Purpose:", lead["purpose"])
    print("Selected Property:", lead["requirements"])
    print("Score:", lead["qualification_score"])
    print("Summary:", lead["conversation_summary"])