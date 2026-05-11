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
Last updated: 2026-05-11 (UTC)

- [Hardware Attestation as Monopoly Enabler](https://grapheneos.social/@GrapheneOS/116550899908879585)
- [Local AI needs to be the norm](https://unix.foo/posts/local-ai-needs-to-be-norm/)
- [The Greatest Shot in Television: James Burke Had One Chance to Nail This Scene (2024)](https://www.openculture.com/2024/10/the-greatest-shot-in-television.html)
- [I'm going back to writing code by hand](https://blog.k10s.dev/im-going-back-to-writing-code-by-hand/)
- [Running local models on an M4 with 24GB memory](https://jola.dev/posts/running-local-models-on-m4)
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
