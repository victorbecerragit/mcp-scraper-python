# mcp_scrape_hackernews

Small CLI scraper for Hacker News top stories. The script accepts a site URL, the number of items, and a CSS selector for titles/links, and prints results as a bullet list.

## MCP Setup Notes

- MCP configuration: .continue/config.json
- Prompt used to create the initial scraper:
  - "add a scrape.py that take as input SITE(HackerNews default) NUM(top 5 default) STYLE(CSS default)"

## Usage

Install dependencies:

```
pip install -r requirements.txt
```

Local run:

```
python app/scrape.py
```

From app directory:

```
cd app
pip install -r requirements.txt
python scrape.py
```

Custom inputs:

```
python app/scrape.py --site https://news.ycombinator.com/ --num 5 --style "tr.athing td.title > span.titleline > a"
```

Timeout/retry options:

```
python app/scrape.py --timeout 30 --retries 3
```

Query mode (search engine):

```
python app/scrape.py --query "top kubernetes vulnerabilities"
```

DuckDuckGo mode:

```
python app/scrape.py --engine duckduckgo --query "top kubernetes vulnerabilities"
```

JSON output:

```
python app/scrape.py --query "top kubernetes vulnerabilities" --output json
```

Note: Google may throttle or block automated requests. If that happens, try DuckDuckGo or provide a direct target URL.

Google fallback:

If Google returns no results, the scraper automatically falls back to DuckDuckGo.

## Docker

Build and run:

```
docker build -t hn-scraper .

docker run --rm hn-scraper
```

Override args:

```
docker run --rm hn-scraper --num 10
```

Example output:

```text
- Create value for others and don’t worry about the returns — https://geohot.github.io//blog/jekyll/update/2026/03/11/running-69-agents.html
- Zig – Type Resolution Redesign and Language Changes — https://ziglang.org/devlog/2026/#2026-03-10
- U+237C ⍼ Is Azimuth — https://ionathan.ch/2026/02/16/angzarr.html
- Julia Snail – An Emacs Development Environment for Julia Like Clojure's Cider — https://github.com/gcv/julia-snail
- Cloudflare crawl endpoint — https://developers.cloudflare.com/changelog/post/2026-03-10-br-crawl-endpoint/
```

Example JSON output:

```json
[
  {
    "title": "OWASP Kubernetes Top Ten",
    "url": "https://owasp.org/www-project-kubernetes-top-ten/"
  },
  {
    "title": "Official CVE Feed - Kubernetes",
    "url": "https://kubernetes.io/docs/reference/issues-security/official-cve-feed/"
  },
  {
    "title": "Top 10 Kubernetes Security Issues - SentinelOne",
    "url": "https://www.sentinelone.com/cybersecurity-101/cloud-security/kubernetes-security-issues/"
  }
]
```
