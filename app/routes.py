from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

# Import services (your real logic)
from app.services.data_service import crawl_site, load_events, set_target_site, get_target_site
from app.services.learning_service import train, score
from app.services.reporting_service import generate

# Import Pydantic models (for structured responses)
from app.models import TrainResult, ReportSummary

# Create a router (group of routes)
router = APIRouter()

# -------------------------------
# Health check
# -------------------------------
@router.get("/")
def root():
    return {"ok": True, "target_site": get_target_site()}


# -------------------------------
# 1. Set Target Site
# -------------------------------
@router.post("/set_site")
def api_set_site(payload: dict = Body(...)):
    url = payload.get("url")
    if not url:
        raise HTTPException(400, "Missing 'url'")
    return {"target_site": set_target_site(url)}


# -------------------------------
# 2. Crawl / Ingest Pages
# -------------------------------
@router.post("/ingest/run")
def api_ingest(max_pages: int = 15):
    events = crawl_site(max_pages=max_pages)
    return {"collected": len(events), "target_site": get_target_site()}


# -------------------------------
# 3. Train Model
# -------------------------------
@router.post("/learn/train", response_model=TrainResult)
def api_train():
    events = load_events()
    result = train(events)
    return result


# -------------------------------
# 4. Generate Risk Report
# -------------------------------
@router.post("/report/generate", response_model=ReportSummary)
def api_report():
    events = load_events()
    risks = score(events)
    summary = generate(events, risks)
    return summary


# -------------------------------
# 5. Download Reports
# -------------------------------
@router.get("/report/latest/html")
def api_report_html():
    path = Path("data/reports/latest/report.html")
    if not path.exists():
        raise HTTPException(404, "Report not found; generate first.")
    return FileResponse(path)

@router.get("/report/latest/csv")
def api_report_csv():
    path = Path("data/reports/latest/report.csv")
    if not path.exists():
        raise HTTPException(404, "Report not found; generate first.")
    return FileResponse(path)

@router.get("/report/latest/json")
def api_report_json():
    path = Path("data/reports/latest/report.json")
    if not path.exists():
        raise HTTPException(404, "Report not found; generate first.")
    return FileResponse(path)

