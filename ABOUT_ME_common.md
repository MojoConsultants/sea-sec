

**Big idea:** This tool looks at a website like a careful guard.  
It takes notes about what it sees, learns what “normal” looks like, and points out things that seem risky.

## The three helpers (services)

1. **Data Service — The Note Taker**
   - Visits a website page by page.
   - Writes down simple facts: page address, links it finds, forms (places you can type), and basic safety signs (like if the page uses HTTPS).
   - Saves these notes as **events** (little records).

2. **Learning Service — The Student**
   - Reads many events to learn normal patterns.
   - Uses a simple math model to spot **weird** events (outliers).
   - The more it sees, the smarter it gets.

3. **Reporting Service — The Storyteller**
   - Takes the events and the model’s “weirdness” scores.
   - Makes clear reports with traffic‑light colors (green/yellow/red).
   - You can read the report in a web page (HTML) or open it in a spreadsheet (CSV).

## Changing the website
You can point the tool at any public website.  
Just call **/set_site** with the new address or set `TARGET_SITE_URL` before you run it.

## A simple trip
1. **/ingest/run** — The Note Taker crawls the site and saves events.
2. **/learn/train** — The Student learns from those events.
3. **/report/generate** — The Storyteller makes reports you can read.

That’s it! Three steps: **collect, learn, report**.
