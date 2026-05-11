#!/usr/bin/env python3
"""
Generalized press release scraper.

Pulls every article from a configured site's news section into a single
markdown file. Ships with configs for Anthropic and OpenAI; add more by
appending to the SITES list at the bottom.

Strategy per site:
  1. Walk the sitemap (handling sitemap-index files)
  2. Filter URLs by path prefix(es)
  3. Fetch each article — try plain HTTP first; if the result looks empty
     (JS-rendered shell), fall back to Playwright if available
  4. Extract title / date / body using per-site selectors with sensible
     fallbacks
  5. Sort newest-first and write to <slug>_news.md

Install:
  pip install requests beautifulsoup4 markdownify lxml
  # Optional, for JS-rendered sites like openai.com:
  pip install playwright
  playwright install chromium

Usage:
  python news_scraper.py                  # scrape all configured sites
  python news_scraper.py anthropic        # scrape just one (by slug)
  python news_scraper.py openai anthropic # scrape multiple
"""

from __future__ import annotations

import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Iterable
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as html_to_md

# ---------- optional Playwright fallback ----------

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


REQUEST_DELAY = 0.5
TIMEOUT = 30
HEADERS = {"User-Agent": "PressReleaseArchiver/1.0 (personal archive)"}

# Tags we always strip from article HTML before converting to markdown
NOISE_SELECTORS = ["nav", "footer", "header", "script", "style", "noscript",
                   "aside", "form"]


# ---------- site config ----------

@dataclass
class SiteConfig:
    slug: str                          # used for output filename
    name: str                          # human-readable
    base_url: str                      # e.g. "https://www.anthropic.com"
    sitemap_url: str                   # e.g. "https://www.anthropic.com/sitemap.xml"
    path_prefixes: list[str]           # e.g. ["/news/"]
    # Optional CSS selectors. If unset, we fall back to <main>/<article>/<h1>/etc.
    article_root_selector: str | None = None
    title_selector: str | None = None
    date_selector: str | None = None
    # Substrings of headings that mark the start of trailing "related" sections to strip
    drop_after_heading_substrings: list[str] = field(
        default_factory=lambda: ["related", "more from", "keep reading"]
    )
    # If True, try Playwright when requests returns a thin/empty page
    js_rendered: bool = False
    # Custom URL filter on top of path_prefixes (return True to keep)
    url_filter: Callable[[str], bool] | None = None


# ---------- fetching ----------

def fetch_requests(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    return r.text


_playwright_ctx = None
_playwright_browser = None


def _get_browser():
    """Lazy-start a single Playwright browser, reused across calls."""
    global _playwright_ctx, _playwright_browser
    if _playwright_browser is None:
        _playwright_ctx = sync_playwright().start()
        _playwright_browser = _playwright_ctx.chromium.launch(headless=True)
    return _playwright_browser


def fetch_playwright(url: str) -> str:
    browser = _get_browser()
    page = browser.new_page(user_agent=HEADERS["User-Agent"])
    try:
        page.goto(url, wait_until="networkidle", timeout=TIMEOUT * 1000)
        # Small extra settle for late-hydrating content
        page.wait_for_timeout(500)
        return page.content()
    finally:
        page.close()


def shutdown_playwright():
    global _playwright_ctx, _playwright_browser
    if _playwright_browser is not None:
        _playwright_browser.close()
        _playwright_browser = None
    if _playwright_ctx is not None:
        _playwright_ctx.stop()
        _playwright_ctx = None


def looks_empty(html: str) -> bool:
    """Heuristic: did we get a JS shell with no real content?"""
    soup = BeautifulSoup(html, "html.parser")
    for sel in NOISE_SELECTORS:
        for t in soup.find_all(sel):
            t.decompose()
    text = soup.get_text(" ", strip=True)
    return len(text) < 400


def fetch_article(url: str, js_rendered: bool) -> str:
    """Fetch with requests; fall back to Playwright if the page looks empty."""
    html = fetch_requests(url)
    if (js_rendered or looks_empty(html)) and PLAYWRIGHT_AVAILABLE:
        try:
            return fetch_playwright(url)
        except Exception as e:
            print(f"  ! Playwright fallback failed ({e}); using requests result", file=sys.stderr)
    elif js_rendered and not PLAYWRIGHT_AVAILABLE:
        print("  ! Site needs JS but Playwright isn't installed; result may be empty",
              file=sys.stderr)
    return html


# ---------- sitemap walk ----------

def discover_urls(site: SiteConfig) -> list[str]:
    print(f"[{site.name}] Walking sitemap: {site.sitemap_url}")
    queue = [site.sitemap_url]
    seen: set[str] = set()
    found: set[str] = set()

    while queue:
        sm_url = queue.pop()
        if sm_url in seen:
            continue
        seen.add(sm_url)
        try:
            xml = fetch_requests(sm_url)
        except Exception as e:
            print(f"  ! Failed {sm_url}: {e}", file=sys.stderr)
            continue
        soup = BeautifulSoup(xml, "xml")

        for sm in soup.find_all("sitemap"):
            loc = sm.find("loc")
            if loc:
                queue.append(loc.get_text(strip=True))

        for u in soup.find_all("url"):
            loc = u.find("loc")
            if not loc:
                continue
            url = loc.get_text(strip=True)
            path = urlparse(url).path
            if not any(path.startswith(p) for p in site.path_prefixes):
                continue
            if path in site.path_prefixes:   # skip the index page itself
                continue
            if site.url_filter and not site.url_filter(url):
                continue
            found.add(url)

        time.sleep(REQUEST_DELAY)

    return sorted(found)


# ---------- parsing ----------

DATE_PATTERNS = [
    (re.compile(r"^[A-Z][a-z]{2,9}\s+\d{1,2},\s+\d{4}$"),
     ["%b %d, %Y", "%B %d, %Y"]),
    (re.compile(r"^\d{4}-\d{2}-\d{2}$"),
     ["%Y-%m-%d"]),
    (re.compile(r"^\d{1,2}\s+[A-Z][a-z]{2,9}\s+\d{4}$"),
     ["%d %b %Y", "%d %B %Y"]),
]


def parse_date(text: str):
    text = text.strip()
    for pattern, formats in DATE_PATTERNS:
        if pattern.match(text):
            for fmt in formats:
                try:
                    return datetime.strptime(text, fmt).date()
                except ValueError:
                    continue
    return None


def find_date(root: Tag) -> tuple[str | None, datetime | None]:
    # <time datetime="..."> is the most reliable signal when present
    for t in root.find_all("time"):
        dt = t.get("datetime")
        if dt:
            for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
                        "%Y-%m-%dT%H:%M:%S.%fZ"):
                try:
                    d = datetime.strptime(dt[:len(fmt) if "T" in fmt else 10], fmt).date()
                    return t.get_text(strip=True) or dt[:10], d
                except ValueError:
                    continue
        txt = t.get_text(strip=True)
        d = parse_date(txt)
        if d:
            return txt, d

    # Otherwise scan early text nodes for a date-shaped string
    for tag in root.find_all(["p", "span", "div"], limit=120):
        txt = tag.get_text(strip=True)
        d = parse_date(txt)
        if d:
            return txt, d
    return None, None


def parse_article(html: str, url: str, site: SiteConfig) -> dict | None:
    soup = BeautifulSoup(html, "html.parser")

    # Find the article root
    root: Tag | None = None
    if site.article_root_selector:
        root = soup.select_one(site.article_root_selector)
    if root is None:
        root = soup.find("article") or soup.find("main")
    if root is None:
        return None

    # Strip noise
    for sel in NOISE_SELECTORS:
        for t in root.find_all(sel):
            t.decompose()

    # Title
    title = None
    if site.title_selector:
        el = root.select_one(site.title_selector) or soup.select_one(site.title_selector)
        if el:
            title = el.get_text(strip=True)
    if not title:
        h1 = root.find("h1") or soup.find("h1")
        title = h1.get_text(strip=True) if h1 else url.rsplit("/", 1)[-1]

    # Date
    date_str, parsed_date = None, None
    if site.date_selector:
        el = root.select_one(site.date_selector) or soup.select_one(site.date_selector)
        if el:
            txt = el.get("datetime") or el.get_text(strip=True)
            parsed_date = parse_date(txt)
            date_str = el.get_text(strip=True) or txt
    if not parsed_date:
        date_str, parsed_date = find_date(root)

    # Drop trailing "Related content" / "More from" sections
    for h in root.find_all(["h2", "h3"]):
        label = h.get_text(strip=True).lower()
        if any(s in label for s in site.drop_after_heading_substrings):
            for sib in list(h.next_siblings):
                if hasattr(sib, "decompose"):
                    sib.decompose()
            h.decompose()
            break

    # Remove the title element from the body so we don't duplicate it
    for h1 in root.find_all("h1"):
        h1.decompose()

    body_md = html_to_md(str(root), heading_style="ATX").strip()
    body_md = re.sub(r"\n{3,}", "\n\n", body_md)

    return {
        "url": url,
        "title": title,
        "date_str": date_str or "Unknown date",
        "date": parsed_date or datetime.min.date(),
        "body": body_md,
    }


# ---------- driver ----------

def scrape_site(site: SiteConfig) -> str:
    urls = discover_urls(site)
    print(f"[{site.name}] Found {len(urls)} article URLs\n")

    articles = []
    for i, url in enumerate(urls, 1):
        print(f"[{site.name}] [{i}/{len(urls)}] {url}")
        try:
            html = fetch_article(url, site.js_rendered)
            article = parse_article(html, url, site)
            if article:
                articles.append(article)
            else:
                print("  ! Couldn't locate article body")
        except Exception as e:
            print(f"  ! Failed: {e}", file=sys.stderr)
        time.sleep(REQUEST_DELAY)

    articles.sort(key=lambda a: a["date"], reverse=True)

    out_path = f"{site.slug}_news.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# {site.name} Press Releases\n\n")
        f.write(f"_Scraped from {site.base_url} on {datetime.now().date().isoformat()}_  \n")
        f.write(f"_{len(articles)} articles, newest first_\n\n")
        f.write("---\n\n")
        for a in articles:
            f.write(f"## {a['title']}\n\n")
            f.write(f"**Date:** {a['date_str']}  \n")
            f.write(f"**Source:** {a['url']}\n\n")
            f.write(a["body"])
            f.write("\n\n---\n\n")

    print(f"[{site.name}] Wrote {len(articles)} articles to {out_path}\n")
    return out_path


# ---------- site configurations ----------

SITES: list[SiteConfig] = [
    SiteConfig(
        slug="anthropic",
        name="Anthropic",
        base_url="https://www.anthropic.com",
        sitemap_url="https://www.anthropic.com/sitemap.xml",
        path_prefixes=["/news/"],
        js_rendered=False,
    ),
    SiteConfig(
        slug="openai",
        name="OpenAI",
        base_url="https://openai.com",
        sitemap_url="https://openai.com/sitemap.xml",
        # OpenAI's blog/news lives under several prefixes — adjust as needed
        # after a first run. /index/ is their main news index.
        path_prefixes=["/index/", "/blog/"],
        js_rendered=True,  # JS-rendered, needs Playwright
        # OpenAI filing pages and other non-article paths can sneak in;
        # exclude obvious non-articles here if you spot them.
        url_filter=lambda u: not any(
            seg in u for seg in ["/research/", "/careers/", "/policies/"]
        ),
    ),
]


def main(argv: list[str]):
    selected = SITES
    if len(argv) > 1:
        wanted = set(argv[1:])
        selected = [s for s in SITES if s.slug in wanted]
        unknown = wanted - {s.slug for s in SITES}
        if unknown:
            print(f"Unknown site(s): {', '.join(sorted(unknown))}", file=sys.stderr)
            print(f"Available: {', '.join(s.slug for s in SITES)}", file=sys.stderr)
            sys.exit(1)

    try:
        for site in selected:
            scrape_site(site)
    finally:
        shutdown_playwright()


if __name__ == "__main__":
    main(sys.argv)
