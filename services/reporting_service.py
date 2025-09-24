import os
import json
from typing import List
from pathlib import Path
from typing import List
from pathlib import Path
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML
from models.events import SecurityEvent, ReportSummary
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML
from models.events import SecurityEvent, ReportSummary
from typing import Optional
from pydantic import BaseModel

DATA_DIR = Path(os.getenv("DATA_DIR", "data")).resolve()
REPORTS_DIR = DATA_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

def generate(events: List[SecurityEvent], risk_scores) -> ReportSummary: # type: ignore
    if not events:
        raise ValueError("No events to report.")
    
    # Prepare DataFrame
    df = pd.DataFrame([e.model_dump() for e in events])
    df["risk"] = risk_scores
    df = df.sort_values("risk", ascending=False)

    # Create report directory
    latest = REPORTS_DIR / "latest"
    latest.mkdir(parents=True, exist_ok=True)

    # CSV and JSON exports
    csv_path = latest / "report.csv"
    json_path = latest / "report.json"
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2, date_format="iso")

    # HTML report from Jinja2 template
    template = env.get_template("report.html.j2")
    html = template.render(rows=df.to_dict(orient="records"))
    html_path = latest / "report.html"
    html_path.write_text(html, encoding="utf-8")

    # HTML → PDF
    pdf_path = latest / "report.pdf"
    HTML(string=html).write_pdf(str(pdf_path))

    # HTML → PNG (requires Cairo backend)
    png_path = latest / "report.png"
    try:
        HTML(string=html).write_png(str(png_path))
    except Exception as e:
        png_path = None
        print(f"[WARN] PNG export failed: {e}  Untitled1:62 - reporting_service.py:62")



class ReportSummary(BaseModel):
    total_events: int
    anomalies: int
    report_html_path: str
    report_csv_path: str
    report_json_path: str
    report_pdf_path: Optional[str] = None
    report_png_path: Optional[str] = None

DATA_DIR = Path(os.getenv("DATA_DIR", "data")).resolve()
REPORTS_DIR = DATA_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

def generate(events: List[SecurityEvent], risk_scores) -> ReportSummary:
    if not events:
        raise ValueError("No events to report.")
    
    # Prepare DataFrame
    df = pd.DataFrame([e.model_dump() for e in events])
    df["risk"] = risk_scores
    df = df.sort_values("risk", ascending=False)

    # Create report directory
    latest = REPORTS_DIR / "latest"
    latest.mkdir(parents=True, exist_ok=True)

    # CSV and JSON exports
    csv_path = latest / "report.csv"
    json_path = latest / "report.json"
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2, date_format="iso")

    # HTML report from Jinja2 template
    template = env.get_template("report.html.j2")
    html = template.render(rows=df.to_dict(orient="records"))
    html_path = latest / "report.html"
    html_path.write_text(html, encoding="utf-8")

    # HTML → PDF
    pdf_path = latest / "report.pdf"
    HTML(string=html).write_pdf(str(pdf_path))

    # HTML → PNG (requires Cairo backend)
    png_path = latest / "report.png"
    try:
        HTML(string=html).write_png(str(png_path))
    except Exception as e:
        png_path = None
        print(f"[WARN] PNG export failed: {e}  Untitled1:119 - reporting_service.py:119")

    return ReportSummary(
        total_events=len(events),
        anomalies=int((df["risk"] > 0.8).sum()),
        report_html_path=str(html_path),
        report_csv_path=str
