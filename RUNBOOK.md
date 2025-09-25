# SEA-SEC Runbook

This runbook explains how to build and run the SEA-SEC application inside Docker.

---

## 📦 Prerequisites
- Docker installed (https://docs.docker.com/get-docker/)
- Docker Compose (newer Docker Desktop already includes it)
- Clone or download the SEA-SEC repo

---

## 🚀 Running SEA-SEC

### Step 1. Make the script executable
```bash
chmod +x run-sea-seq.sh


Reports are saved to:

./reports/report.html → colored HTML report

./reports/report.csv → CSV data

./reports/report.json → JSON data

🛑 Stopping SEA-SEC

Press CTRL + C or run:


docker compose down --volumes --remove-orphans
docker compose build --no-cache


---

# 📄 `run-sea-seq.sh`

Place this file at the root of your project (`Sea-Seq V.01/run-sea-seq.sh`):

```bash
#!/bin/bash
set -e

echo "🔄 Building SEA-SEC Docker image..."
docker compose build

echo "🚀 Starting SEA-SEC container..."
docker compose up

