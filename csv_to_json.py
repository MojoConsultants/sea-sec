#!/usr/bin/env python3
"""
Site Metadata Crawler
---------------------
Crawls all pages of a given site, extracts metadata + resolved IP address,
and exports results into a CSV file for security testing / STTS tracking.

✅ Features:
- Always saves output to the same folder as this script
- Prints debug info including full file path
- Shows "Status = 200" messages for successful page fetches
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import socket
import csv
import os

# ========== CONFIGURATION ==========
BASE_URL = "https://mlbam-park.b12sites.com/index"
OUTPUT_FILE = "site_metadata.csv"
TIMEOUT = 10
# ===================================

# Get the directory where this script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, OUTPUT_FILE)


def resolve_ip(url: str) -> str:
    """Resolve the domain name into an IP address"""
    try:
        domain = urlparse(url).hostname
        return socket.gethostbyname(domain)
    except Exception as e:
        print(f"[!] Error resolving IP: {e} - csv_to_json.py:38")
        return "N/A"


def extract_metadata(soup: BeautifulSoup) -> dict:
    """Extract metadata tags from a web page"""
    return {
        "Title": soup.title.string.strip() if soup.title and soup.title.string else "",
        "Meta Description": (soup.find("meta", attrs={"name": "description"}) or {}).get("content", ""),
        "Meta Keywords": (soup.find("meta", attrs={"name": "keywords"}) or {}).get("content", ""),
        "Robots": (soup.find("meta", attrs={"name": "robots"}) or {}).get("content", "")
    }


def crawl_site(base_url: str, ip_address: str) -> list:
    """Visit the site, follow internal links, and collect metadata"""
    visited = set()
    to_visit = [base_url]
    results = []
    base_domain = urlparse(base_url).netloc  # Only crawl this domain

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)

        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code == 200:
                print(f"[*] Fetching {url} > Status = 200 ✅ - csv_to_json.py:68")
            else:
                print(f"[!] Skipped {url} (status {response.status_code}) - csv_to_json.py:70")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            metadata = extract_metadata(soup)
            metadata.update({"Page URL": url, "Hosting IP": ip_address})
            results.append(metadata)

            # Find and queue new links
            for link in soup.find_all("a", href=True):
                new_url = urljoin(url, link["href"])
                if urlparse(new_url).netloc == base_domain and new_url not in visited:
                    to_visit.append(new_url)

        except Exception as e:
            print(f"[!] Error fetching {url}: {e} - csv_to_json.py:86")

    return results


def save_to_csv(data: list, filename: str):
    """Save collected metadata into a CSV file"""
    if not data:
        print("[!] No data to save. - csv_to_json.py:94")
        return

    keys = ["Page URL", "Title", "Meta Description", "Meta Keywords", "Robots", "Hosting IP"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"[+] Export complete. File saved at: {filename} - csv_to_json.py:103")


if __name__ == "__main__":
    print("[*] Starting metadata crawler... - csv_to_json.py:107")
    ip_address = resolve_ip(BASE_URL)
    print(f"[+] Resolved IP: {ip_address} - csv_to_json.py:109")

    results = crawl_site(BASE_URL, ip_address)
    save_to_csv(results, CSV_FILE)

    print("[✓] Done. Metadata collection finished. - csv_to_json.py:114")
