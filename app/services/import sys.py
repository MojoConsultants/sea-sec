# ===============================
# Chapter 1: Imports and Setup
# ===============================
# This chapter sets up the environment and dependencies for unit testing and patching.
import sys
import json
import csv
from pathlib import Path
import pytest

# ===============================
# Chapter 2: Importing Reporting Service
# ===============================
# Import the function to test
import app.services.reporting_service as reporting_service

# Patch _get_risk_reason since it's not defined in the module
# Developer Note: This is a test stub for risk reason logic.
def _get_risk_reason(event, risk):
    return ("UnitTest Reason", "UnitTest Description")

reporting_service._get_risk_reason = _get_risk_reason

# ===============================
# Chapter 3: Dummy Event for Testing
# ===============================
class DummyEvent:
    def __init__(self, timestamp, page_url, https, num_links, num_forms, has_login_form):
        self.timestamp = timestamp
        self.page_url = page_url
        self.https = https
        self.num_links = num_links
        self.num_forms = num_forms
        self.has_login_form = has_login_form

# ===============================
# Chapter 4: Pytest Fixtures
# ===============================
@pytest.fixture
def sample_events_and_risks(tmp_path, monkeypatch):
    # Patch REPORT_DIR to use a temp directory
    monkeypatch.setattr(reporting_service, "REPORT_DIR", tmp_path)
    events = [
        DummyEvent("2024-06-01T12:00:00", "http://site1.com", True, 5, 2, False),
        DummyEvent("2024-06-01T13:00:00", "http://site2.com", False, 10, 1, True),
        DummyEvent("2024-06-01T14:00:00", "http://site3.com", True, 2, 0, False),
    ]
    risks = [
        {"event": events[0], "risk": 3},
        {"event": events[1], "risk": 8},
        {"event": events[2], "risk": 5},
    ]
    return events, risks, tmp_path

# ===============================
# Chapter 5: Main Test
# ===============================
def test_generate_creates_files_and_returns_correct_counts(sample_events_and_risks):
    events, risks, report_dir = sample_events_and_risks
    result = reporting_service.generate(events, risks)
    assert result["total_events"] == 3
    assert result["anomalies"] == 1

    # Check files exist
    json_path = report_dir / "report.json"
    csv_path = report_dir / "report.csv"
    html_path = report_dir / "report.html"
    assert json_path.exists()
    assert csv_path.exists()
    assert html_path.exists()

def test_json_file_content(sample_events_and_risks):
    events, risks, report_dir = sample_events_and_risks
    reporting_service.generate(events, risks)
    json_path = report_dir / "report.json"
    with open(json_path) as f:
        data = json.load(f)
    assert len(data) == 3
    assert data[0]["risk_level"] == "Low"
    assert data[1]["risk_level"] == "High"
    assert data[2]["risk_level"] == "Medium"
    assert all("UnitTest Reason" == d["risk_reason"] for d in data)
    assert all("UnitTest Description" == d["description"] for d in data)

def test_csv_file_content(sample_events_and_risks):
    events, risks, report_dir = sample_events_and_risks
    reporting_service.generate(events, risks)
    csv_path = report_dir / "report.csv"
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 3
    assert rows[0]["risk_level"] == "Low"
    assert rows[1]["risk_level"] == "High"
    assert rows[2]["risk_level"] == "Medium"

def test_html_file_content(sample_events_and_risks):
    events, risks, report_dir = sample_events_and_risks
    reporting_service.generate(events, risks)
    html_path = report_dir / "report.html"
    with open(html_path) as f:
        html = f.read()
    assert "SEA-SEC Risk Report" in html
    assert "UnitTest Reason" in html
    assert "UnitTest Description" in html
    assert "class=\"high\"" in html
    assert "class=\"medium\"" in html
    assert "class=\"low\"" in html