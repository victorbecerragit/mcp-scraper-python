import unittest

from app import scrape


class TestScrape(unittest.TestCase):
    def test_scrape_default_selector(self) -> None:
        html = scrape.fetch_html(scrape.DEFAULT_SITE)
        titles = scrape.scrape_titles(html, scrape.DEFAULT_STYLE)
        self.assertTrue(titles, "Expected at least one title")
        self.assertGreaterEqual(len(titles), 5)
        for title, href in titles[:5]:
            self.assertTrue(title)
            self.assertTrue(href)


if __name__ == "__main__":
    unittest.main()
