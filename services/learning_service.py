from typing import List, Dict, Any
from app.services.risk_rules import contains_financial_data, contains_phi_data

def score(events: List[Any]) -> List[Dict[str, Any]]:
    results = []

    for event in events:
        risk = 0

        # Example base rules
        if getattr(event, "has_login_form", False):
            risk += 2
        if getattr(event, "https", True) is False:
            risk += 3

        # Sensitive data rules 🚨
        if contains_financial_data(event) or contains_phi_data(event):
            risk = 10  # force high risk

        # Clamp to 10 max
        risk = min(risk, 10)

        results.append({"event": event, "risk": risk})

    return results





