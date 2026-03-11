#!/usr/bin/env python3
"""Scrape Hacker News headlines with a CSS selector.

Defaults:
- site: https://news.ycombinator.com/
- num: 5
- style: tr.athing td.title > span.titleline > a
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from typing import List, Tuple

DEFAULT_SITE = "https://news.ycombinator.com/"
DEFAULT_STYLE = "tr.athing td.title > span.titleline > a"
DEFAULT_ENGINE = "google"
DEFAULT_GOOGLE_STYLE = "a h3"
DEFAULT_DDG_STYLE = "a.result__a"


def fetch_html(url: str, timeout: int, retries: int) -> str:
    last_error: Exception | None = None
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = response.read()
                encoding = response.headers.get("Content-Encoding", "").lower()
                if encoding in {"gzip", "x-gzip"}:
                    import gzip

                    data = gzip.decompress(data)
                elif encoding == "br":
                    try:
                        import brotli
                    except ImportError as exc:
                        raise RuntimeError(
                            "Brotli response received. Install 'brotli' to decode it."
                        ) from exc
                    data = brotli.decompress(data)
                elif encoding == "deflate":
                    import zlib

                    data = zlib.decompress(data)
                return data.decode("utf-8", errors="replace")
        except Exception as exc:
            last_error = exc
            if attempt >= retries:
                break

    raise RuntimeError(f"Failed to fetch {url}: {last_error}")


def normalize_google_href(href: str) -> str:
    if not href:
        return ""
    if href.startswith("/url?"):
        parsed = urllib.parse.urlsplit(href)
        params = urllib.parse.parse_qs(parsed.query)
        return params.get("q", [""])[0]
    if href.startswith("http"):
        return href
    return ""


def normalize_duckduckgo_href(href: str) -> str:
    if not href:
        return ""
    if href.startswith("//duckduckgo.com/l/?"):
        href = "https:" + href
    if href.startswith("https://duckduckgo.com/l/?"):
        parsed = urllib.parse.urlsplit(href)
        params = urllib.parse.parse_qs(parsed.query)
        return params.get("uddg", [""])[0]
    if href.startswith("http"):
        return href
    return ""


def scrape_titles(html: str, style: str, engine: str | None = None) -> List[Tuple[str, str]]:
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:
        raise RuntimeError(
            "BeautifulSoup is required for CSS selector support. "
            "Install it with: pip install -r requirements.txt"
        ) from exc

    soup = BeautifulSoup(html, "html.parser")
    titles: List[Tuple[str, str]] = []

    if engine == "google" and style == DEFAULT_GOOGLE_STYLE:
        for header in soup.select(style):
            anchor = header.parent if header.parent and header.parent.name == "a" else None
            if not anchor:
                continue
            text = header.get_text(strip=True)
            href = normalize_google_href(anchor.get("href") or "")
            if text and href:
                titles.append((text, href))
        return titles

    if engine == "duckduckgo" and style == DEFAULT_DDG_STYLE:
        for link in soup.select(style):
            text = link.get_text(strip=True)
            href = normalize_duckduckgo_href(link.get("href") or "")
            if text and href:
                titles.append((text, href))
        return titles

    for link in soup.select(style):
        text = link.get_text(strip=True)
        href = link.get("href") or ""
        if text:
            titles.append((text, href))

    return titles


def build_search_url(engine: str, query: str, num: int) -> str:
    if engine == "google":
        params = urllib.parse.urlencode({"q": query, "hl": "en", "num": str(num), "gbv": "1"})
        return f"https://www.google.com/search?{params}"
    if engine == "duckduckgo":
        params = urllib.parse.urlencode({"q": query})
        return f"https://html.duckduckgo.com/html/?{params}"
    raise ValueError(f"Unsupported engine: {engine}")


def default_style_for_engine(engine: str) -> str:
    if engine == "google":
        return DEFAULT_GOOGLE_STYLE
    if engine == "duckduckgo":
        return DEFAULT_DDG_STYLE
    raise ValueError(f"Unsupported engine: {engine}")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape Hacker News headlines.")
    parser.add_argument("--site", default=DEFAULT_SITE, help="Target URL.")
    parser.add_argument(
        "--query",
        default=None,
        help="Search query to run on the selected engine.",
    )
    parser.add_argument(
        "--engine",
        default=DEFAULT_ENGINE,
        help="Search engine for query mode (google, duckduckgo).",
    )
    parser.add_argument("--num", type=int, default=5, help="Number of items to print.")
    parser.add_argument("--timeout", type=int, default=20, help="Request timeout in seconds.")
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="Retry count for failed requests.",
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--style",
        default=None,
        help="CSS selector for titles/links.",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    try:
        if args.query:
            url = build_search_url(args.engine, args.query, args.num)
            style = args.style or default_style_for_engine(args.engine)
            html = fetch_html(url, args.timeout, args.retries)
            titles = scrape_titles(html, style, engine=args.engine)
            if not titles and args.engine == "google":
                fallback_engine = "duckduckgo"
                url = build_search_url(fallback_engine, args.query, args.num)
                style = args.style or default_style_for_engine(fallback_engine)
                html = fetch_html(url, args.timeout, args.retries)
                titles = scrape_titles(html, style, engine=fallback_engine)
        else:
            url = args.site
            style = args.style or DEFAULT_STYLE
            html = fetch_html(url, args.timeout, args.retries)
            titles = scrape_titles(html, style)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not titles:
        print(
            "No results found. The target site may be blocking automated requests. "
            "Try a different engine or provide a direct URL.",
            file=sys.stderr,
        )

    if args.output == "json":
        payload = [{"title": t, "url": u} for t, u in titles[: args.num]]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    for title, href in titles[: args.num]:
        print(f"- {title} — {href}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
