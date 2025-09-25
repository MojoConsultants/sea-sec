# ===============================
# Chapter 1: Imports and Setup
# ===============================
# This chapter sets up the environment and dependencies for data collection and event processing.
import os, re, json, time
from typing import List, Tuple
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from models.events import SecurityEvent
from pathlib import Path

DATA_DIR = Path(os.getenv("DATA_DIR", "data")).resolve()
EVENTS_PATH = DATA_DIR / "events.jsonl"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_SITE = os.getenv("TARGET_SITE_URL", "https://mlbam-park.b12sites.com/").strip()

# ===============================
# Chapter 2: Target Site Management
# ===============================
def get_target_site() -> str:
    """Developer Note: Returns the current target site for scanning."""
    site_file = DATA_DIR / "target_site.txt"
    if site_file.exists():
        return site_file.read_text().strip()
    return DEFAULT_SITE

def set_target_site(url: str) -> str:
    """Developer Note: Sets the target site for scanning."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "target_site.txt").write_text(url.strip())
    return url.strip()

# ===============================
# Chapter 3: Event Fetching and Parsing
# ===============================
def _fetch(url: str) -> Tuple[str, requests.Response]:
    """Developer Note: Fetches a URL and returns the response."""
    r = requests.get(url, timeout=15, headers={"User-Agent":"SEA-SEC/0.1"})
    r.raise_for_status()
    return url, r

def _event_from_response(url: str, r: requests.Response) -> SecurityEvent:
    """Developer Note: Parses a response into a SecurityEvent object."""
    https = urlparse(url).scheme == "https"
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find_all("a")
    forms = soup.find_all("form")
    has_login = any("password" in (inp.get("type","").lower()) for f in forms for inp in f.find_all("input"))
    headers = {k:str(v) for k,v in r.headers.items() if k.lower() in {"server","content-type","x-powered-by"}}
    return SecurityEvent(page_url=url, https=https, num_links=len(links), num_forms=len(forms), has_login_form=has_login, headers=headers)

# ===============================
# Chapter 4: Vulnerability Reports (Future)
# ===============================
def explotsreports():
    """
    Developer Note: This function will process quarterly exploit reports and feed them into the vulnerability engine.
    Steps:
    1. Intake quarterly reports
    2. Parse for vulnerabilities
    3. Align vulnerabilities to tiers
    4. Store in database
    5. Provide to engine, frontend, and API
    """
    pass

# ===============================
# Chapter 5: Site Crawling
# ===============================
def crawl_site(max_pages: int = 15) -> List[SecurityEvent]:
    start = get_target_site()
    seen = set()
    to_visit = [start]
    events: List[SecurityEvent] = []
    while to_visit and len(seen) < max_pages:
        url = to_visit.pop(0)
        if url in seen:
            continue
        seen.add(url)
        try:
            _, resp = _fetch(url)
            ev = _event_from_response(url, resp)
            events.append(ev)
            # enqueue new links on same host
            soup = BeautifulSoup(resp.text, "html.parser")
            base = f"{urlparse(start).scheme}://{urlparse(start).netloc}"
            for a in soup.find_all("a", href=True):
                nxt = urljoin(url, a["href"])
                if urlparse(nxt).netloc == urlparse(start).netloc:
                    if nxt not in seen and nxt not in to_visit:
                        to_visit.append(nxt)
        except Exception as e:
            events.append(SecurityEvent(page_url=url, https=urlparse(url).scheme=="https",
                                        num_links=0, num_forms=0, has_login_form=False,
                                        headers={}, note=f"error: {type(e).__name__}: {e}"))
        time.sleep(0.3)
    # persist
    with open(EVENTS_PATH, "a") as f:
        for ev in events:
            f.write(ev.model_dump_json() + "\n")
    return events

# ===============================
# Chapter 6: Event Loading
# ===============================
def load_events(limit: int = None) -> List[SecurityEvent]:
    events = []
    if not EVENTS_PATH.exists():
        return events
    with open(EVENTS_PATH) as f:
        for i, line in enumerate(f):
            try:
                events.append(SecurityEvent.model_validate_json(line))
            except Exception:
                continue
            if limit and len(events) >= limit:
                break
    return events
