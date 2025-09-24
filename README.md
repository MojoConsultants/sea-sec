# SEA-SEC Demo (Mansa Park)
A small, self-contained security analysis demo you can point at any public site (default: https://mlbam-park.b12sites.com/).

## Services
- **Data Service**: fetches pages, forms, links, and simple headers; normalizes into `SecurityEvent` records.
- **Learning Service**: trains a tiny anomaly model on observed events to learn patterns.
- **Reporting Service**: creates human-friendly HTML/CSV/JSON reports with risk highlights.

## Quick Start

### 1) Python
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# set target site (defaults to MLBAM Park demo site)
export TARGET_SITE_URL="https://mlbam-park.b12sites.com/"

# run the API
uvicorn app:app --reload --port 8000
```

### 2) Endpoints
- `POST /set_site` body: `{ "url": "https://example.com" }` — change target
- `POST /ingest/run` — crawl & collect security events
- `POST /learn/train` — fit/update model from collected events
- `POST /report/generate` — build HTML/CSV/JSON under `./data/reports/`
- `GET /report/latest/html` — serve the latest HTML report

### 3) Docker
```bash
docker build -t sea-sec-demo .
docker run -p 8000:8000 -e TARGET_SITE_URL="https://mlbam-park.b12sites.com/" sea-sec-demo
```

## Folder layout
```
services/          # data, learning, reporting services
models/            # data models (pydantic)
templates/         # report HTML template
data/              # collected events, models, reports
```

See `ABOUT_ME_common.md` for a kid-friendly explainer.
