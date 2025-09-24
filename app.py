import os
from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
from services.data_service import crawl_site, load_events, set_target_site, get_target_site
from services.learning_service import train, score
from services.reporting_service import generate
from models.events import TrainResult, ReportSummary
from pathlib import Path

app = FastAPI(title="SEA-SEC Demo", version="0.1")

@app.get("/")
def root():
    return {"ok": True, "target_site": get_target_site()}

@app.post("/set_site")
def api_set_site(payload: dict = Body(...)):
    url = payload.get("url")
    if not url:
        raise HTTPException(400, "Missing 'url'")
    return {"target_site": set_target_site(url)}

@app.post("/ingest/run")
def api_ingest(max_pages: int = 15):
    events = crawl_site(max_pages=max_pages)
    return {"collected": len(events), "target_site": get_target_site()}

@app.post("/learn/train", response_model=TrainResult)
def api_train():
    events = load_events()
    result = train(events)
    return result

@app.post("/report/generate", response_model=ReportSummary)
def api_report():
    events = load_events()
    risks = score(events)
    summary = generate(events, risks)
    return summary

@app.get("/report/latest/html")
def api_report_html():
    path = Path("data/reports/latest/report.html")
    if not path.exists():
        raise HTTPException(404, "Report not found; generate first.")
    return FileResponse(path)

@app.get("/report/latest/csv")
def api_report_csv():
    path = Path("data/reports/latest/report.csv")
    if not path.exists():
        raise HTTPException(404, "Report not found; generate first.")
    return FileResponse(path)

@app.get("/report/latest/json")
def api_report_json():
    path = Path("data/reports/latest/report.json")
    if not path.exists():
        raise HTTPException(404, "Report not found; generate first.")
    return FileResponse(path)
