# SEA-SEQ

SEA-SEQ (Security Event Analysis - SEQuence) is a demo web application that scans public websites for basic security-related signals, learns patterns, and generates risk reports.

## 🚀 Features

- Collects security-relevant metadata from target websites
- Trains a simple anomaly detection model
- Generates HTML, CSV, and JSON reports
- Runs via Docker or locally with Python/FastAPI

## 🔧 Quick Start

### Run via Docker

```bash
chmod +x run-sea-seq.sh
./run-sea-seq.sh
```

### Run via Python

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## 🔌 API Endpoints

- `POST /set_site`
- `POST /ingest/run`
- `POST /learn/train`
- `POST /report/generate`
- `GET  /report/latest/html`

## 📁 Project Structure

- `services/` — data collection, learning, and reporting logic
- `models/` — Pydantic models for events and reports
- `templates/` — Jinja2 report templates
- `data/` — output data directory (events, models, reports)

---
