"""CBC World news scraper."""
import requests
from src.scrape.base import BaseScraper
from src.scrape.rss import parse_rss, render_rss_html


class CBCWorldScraper(BaseScraper):
    ID = "cbc_world"
    LABEL = "🌍 World News"
    SOURCE_URLS = ["https://www.cbc.ca/webfeed/rss/rss-world"]

    def fetch(self) -> dict:
        url = "https://www.cbc.ca/webfeed/rss/rss-world"
        try:
            resp = requests.get(url, timeout=20, allow_redirects=True)
            resp.raise_for_status()
            items = parse_rss(resp.text, limit=6)
            if items:
                html = render_rss_html(items)
                text = "; ".join(item["title"] for item in items)
            else:
                html = '<p>No recent world news.</p>'
                text = "No recent world news."
        except Exception:
            html = '<p>World news feed temporarily unavailable.</p>'
            text = "World news unavailable."
        return self.result(html=html, text=text)


def scrape():
    return CBCWorldScraper()()
