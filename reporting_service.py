import os, json
from weasyprint import HTML
from typing import List
from pathlib import Path
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape
from models.events import SecurityEvent, ReportSummary

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
    df = pd.DataFrame([e.model_dump() for e in events])
    df["risk"] = risk_scores
    df = df.sort_values("risk", ascending=False)


# Generate PDF/PNG from HTML report (using WeasyPrint)
    template = env.get_template("report.html.j2")
    html = template.render(rows=df.to_dict(orient="records"))
    latest = REPORTS_DIR / "latest"
    latest.mkdir(parents=True, exist_ok=True)
    # HTML → PDF
    pdf_path = latest / "report.pdf"
    HTML(string=html).write_pdf(str(pdf_path))

    # HTML → PNG
    png_path = latest / "report.png"
    HTML(string=html).write_png(str(png_path))  # Requires Cairo installed

# Optional: Generate SVG separately if needed

    # write CSV/JSON
    latest = REPORTS_DIR / "latest"
    latest.mkdir(parents=True, exist_ok=True)
    csv_path = latest / "report.csv"
    json_path = latest / "report.json"
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2, date_format="iso")

    # HTML via template
    template = env.get_template("report.html.j2")
    html = template.render(rows=df.to_dict(orient="records"))
    html_path = latest / "report.html"
    html_path.write_text(html, encoding="utf-8")

    return ReportSummary(
    total_events=len(events),
    anomalies=int((df["risk"] > 0.8).sum()),
    report_html_path=str(html_path),
    report_csv_path=str(csv_path),
    report_json_path=str(json_path),
    report_pdf_path=str(pdf_path),
    report_png_path=str(png_path),
    # report_svg_path=str(svg_path 
    # if svg_path else You can add svg_path 
    # if implemented
          


    )
