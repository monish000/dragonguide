"""
download_docs.py — Refresh knowledge base from official Drexel web pages.

Usage:
    python download_docs.py
    python ingest.py
"""

import re
import sys
from pathlib import Path

import requests

DATA_DIR = Path(__file__).parent / "data"

# Official Drexel sources (Provost, Drexel Central, Catalog)
SOURCES = [
    (
        "Drexel_Official_Academic_Calendar_Provost_2025-2026.txt",
        "https://drexel.edu/provost/policies-calendars/academic-calendars",
        "Office of the Provost — Quarter Academic Calendars 2025-2026 and 2026-2027",
    ),
    (
        "Drexel_University_Catalog_Overview.txt",
        "https://catalog.drexel.edu/",
        "Drexel University Catalog — Overview and Writing-Intensive Requirements",
    ),
    (
        "Drexel_Graduate_Academic_Reminders.txt",
        "https://drexel.edu/graduatecollege/news-events/news/2025/September/Academic%20News%20and%20Key%20Reminders%20-%20Fall%202025/",
        "Office of Graduate Studies — Academic Dates and Key Reminders",
    ),
]

HEADERS = {
    "User-Agent": "DragonGuide-Capstone/1.0 (Educational; Drexel CS-591)",
    "Accept": "text/html,application/xhtml+xml",
}


def html_to_text(html: str) -> str:
    """Lightweight HTML → plain text (no extra dependencies)."""
    html = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", html, flags=re.I)
    html = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", html, flags=re.I)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    html = re.sub(r"</p>|</div>|</tr>|</li>|</h[1-6]>", "\n", html, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&#\d+;", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch_and_save(filename: str, url: str, title: str) -> bool:
    out = DATA_DIR / filename
    try:
        resp = requests.get(url, headers=HEADERS, timeout=45)
        resp.raise_for_status()
        body = html_to_text(resp.text)
        if len(body) < 200:
            print(f"  ✘  {filename} — page too short, skipped")
            return False
        header = (
            f"SOURCE: {title}\n"
            f"URL: {url}\n"
            f"DOCUMENT: {filename}\n"
            f"{'=' * 72}\n\n"
        )
        out.write_text(header + body, encoding="utf-8")
        print(f"  ✔  {filename}  ({len(body):,} chars)")
        return True
    except Exception as exc:
        print(f"  ✘  {filename} — {exc}")
        return False


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("\nDragonGuide — Download Official Documents\n")
    ok = sum(fetch_and_save(fn, url, title) for fn, url, title in SOURCES)
    print(f"\nSaved {ok}/{len(SOURCES)} file(s) to data/\n")
    print("Next:  python ingest.py\n")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
