# mcp_scrape_hackernews

Small CLI scraper for Hacker News top stories. The script accepts a site URL, the number of items, and a CSS selector for titles/links, and prints results as a bullet list.

## MCP Setup Notes

- MCP configuration: .continue/config.json
- Web browser MCP server: https://github.com/blazickjp/web-browser-mcp-server
- Initial MCP test prompt:
  - "Use web-browser-mcp-server to scrape top headlines from Hacker News. Extract:"
  - "- Top 5 story titles and links"
  - "- Use CSS: \"tr.athing td.title > span.titleline > a\" for titles/links"
- Prompt used to create the initial scraper:
  - "add a scrape.py that take as input SITE(HackerNews default) NUM(top 5 default) STYLE(CSS default)"

## Usage and Build

See [docs/USAGE.md](docs/USAGE.md) for install, local usage, and Docker steps.

## Weekly Hacker News

<!-- HACKER_NEWS_START -->
Last updated: 2026-09-07 (UTC)

- [Keep Our Servers Running](https://blog.archive.org/2026/09/01/keep-our-servers-running-your-recurring-donation-goes-3x-this-september/)
- [Making a Python interpreter in 1024 bytes](https://austinhenley.com/blog/python1024.html)
- [I'm a seeing-eye dog for a computer](https://claytonwramsey.com/blog/seeing-eye/)
- [It took a year to ship WebAssembly in Anubis](https://anubis.techaro.lol/blog/2026/anubis-wasm/)
- [Ask HN: Fable hacked my piano, can I release the results?](item?id=49577129)
<!-- HACKER_NEWS_END -->

This section is updated weekly by the CI pipeline using the local scraper output.

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
