# ===============================
# Chapter 1: Imports and Setup
# ===============================
# This chapter sets up the environment and dependencies for reporting.
import os
import json
import csv
from pathlib import Path
from typing import List, Dict, Any

from jinja2 import Template  # Ensure jinja2 is installed: pip install jinja2

REPORT_DIR = Path("data/reports/latest")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ===============================
# Chapter 2: Helper Functions
# ===============================
# _get_risk_reason should be defined or imported. Here is a placeholder:
def _get_risk_reason(event, risk):
    """Developer Note: Replace with real logic for risk reason and description."""
    return ("Reason not implemented", "Description not implemented")

# ===============================
# Chapter 3: Main Report Generation
# ===============================
def generate(events: List[Any], risks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate HTML, CSV, and JSON reports including risk score,
    reason, description, and risk level (Low/Medium/High).
    """
    # Attach risk info to events
    enriched = []
    for r in risks:
        event = r["event"]
        risk = r["risk"]

        # Determine reason + description
        reason, description = _get_risk_reason(event, risk)

        # Assign risk level for reporting
        if risk >= 7:
            risk_level = "High"
        elif risk >= 4:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        enriched.append({
            "timestamp": str(event.timestamp) if hasattr(event, "timestamp") else None,
            "page_url": getattr(event, "page_url", None),
            "https": getattr(event, "https", None),
            "num_links": getattr(event, "num_links", None),
            "num_forms": getattr(event, "num_forms", None),
            "has_login_form": getattr(event, "has_login_form", None),
            "risk": risk,
            "risk_level": risk_level,
            "risk_reason": reason,
            "description": description,
        })

    # Write JSON
    json_path = REPORT_DIR / "report.json"
    with open(json_path, "w") as f:
        json.dump(enriched, f, indent=2)

    # Write CSV
    csv_path = REPORT_DIR / "report.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=enriched[0].keys())
        writer.writeheader()
        writer.writerows(enriched)

    # Write HTML with color coding
    html_template = """
    <html>
      <head>
        <title>SEA-SEC Report</title>
        <style>
          .low { background-color: #d4edda; }      /* light green */
          .medium { background-color: #fff3cd; }   /* light yellow */
          .high { background-color: #f8d7da; }     /* light red */
        </style>
      </head>
      <body>
        <h1>SEA-SEC Risk Report</h1>
        <table border="1" cellspacing="0" cellpadding="4">
          <tr>
            {% for col in records[0].keys() %}
              <th>{{ col }}</th>
            {% endfor %}
          </tr>
          {% for row in records %}
            {% set risk = row['risk'] %}
            {% if risk >= 7 %}
              <tr class="high">
            {% elif risk >= 4 %}
              <tr class="medium">
            {% else %}
              <tr class="low">
            {% endif %}
              {% for col, val in row.items() %}
                <td>{{ val }}</td>
              {% endfor %}
            </tr>
          {% endfor %}
        </table>
      </body>
    </html>
    """
    html = Template(html_template).render(records=enriched)
    html_path = REPORT_DIR / "report.html"
    with open(html_path, "w") as f:
        f.write(html)

    # ===============================
    # Chapter 4: Return Summary
    # ===============================
    # Developer Note: This return is for FastAPI endpoints.
    return {
        "total_events": len(events),
        "anomalies": sum(1 for r in enriched if r["risk"] >= 7),
        "report_html_path": str(html_path),
        "report_csv_path": str(csv_path),
        "report_json_path": str(json_path),
        "events": enriched
    }