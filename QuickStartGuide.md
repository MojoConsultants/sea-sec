##Quick Start Guide##

# 1) set up
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) (optional) point to a site — defaults to the MLBAM Park demo
export TARGET_SITE_URL="https://mlbam-park.b12sites.com/"

# 3) run the API
uvicorn app:app --reload --port 8000
