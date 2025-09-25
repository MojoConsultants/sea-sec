import re
from typing import Any

# ======================
# Regex patterns
# ======================
FINANCIAL_PATTERNS = [
    re.compile(r"\b\d{13,16}\b"),              # Credit card (basic)
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),      # SSN (US format)
    re.compile(r"\b\d{9}\b"),                  # Bank account (generic 9 digits)
]

PHI_KEYWORDS = [
    "patient",
    "diagnosis",
    "treatment",
    "medical",
    "record",
    "insurance",
    "icd",
    "lab",
    "test result",
]


# ======================
# Detection helpers
# ======================
def contains_financial_data(event: Any) -> bool:
    """
    Check if the event text or headers contain financial data.
    """
    text = _extract_event_text(event)
    for pattern in FINANCIAL_PATTERNS:
        if pattern.search(text):
            return True
    return False


def contains_phi_data(event: Any) -> bool:
    """
    Check if the event text or headers contain PHI data.
    """
    text = _extract_event_text(event).lower()
    return any(keyword in text for keyword in PHI_KEYWORDS)


# ======================
# Utility
# ======================
def _extract_event_text(event: Any) -> str:
    """
    Flatten event attributes into text for scanning.
    Works with dicts or Pydantic models.
    """
    if isinstance(event, dict):
        parts = []
        for k, v in event.items():
            parts.append(str(v))
        return " ".join(parts)

    # If Pydantic model
    if hasattr(event, "dict"):
        return " ".join(str(v) for v in event.dict().values())

    return str(event)
# ======================
# Dashboard Scoring Events 
# ======================
def score(events):
    results = []
    for event in events:
        risk = 0

        # Base scoring rules (example)
        if event.has_login_form:
            risk += 2
        if not event.https:
            risk += 3

        # Check for financial data
        if contains_financial_data(event):
            risk += 5   # 🚨 raise risk heavily

        # Check for PHI data
        if contains_phi_data(event):
            risk += 5   # 🚨 raise risk heavily

        # Normalize or clamp score
        risk = min(risk, 10)

	#the line below forces high score if either phi and financial 		data is involved.  
	if contains_financial_data(event) or contains_phi_data(event):
    	risk = 10

        results.append({"event": event, "risk": risk})
    return results
