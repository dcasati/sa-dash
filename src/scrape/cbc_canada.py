"""CBC Canada national news scraper."""
import requests
from src.scrape.base import BaseScraper
from src.scrape.rss import parse_rss, render_rss_html


class CBCCanadaScraper(BaseScraper):
    ID = "cbc_canada"
    LABEL = "🍁 Canada News"
    SOURCE_URLS = ["https://www.cbc.ca/webfeed/rss/rss-canada"]

    def fetch(self) -> dict:
        url = "https://www.cbc.ca/webfeed/rss/rss-canada"
        try:
            resp = requests.get(url, timeout=20, allow_redirects=True)
            resp.raise_for_status()
            items = parse_rss(resp.text, limit=6)
            if items:
                html = render_rss_html(items)
                text = "; ".join(item["title"] for item in items)
            else:
                html = '<p>No recent national news.</p>'
                text = "No recent national news."
        except Exception:
            html = '<p>National news feed temporarily unavailable.</p>'
            text = "National news unavailable."
        return self.result(html=html, text=text)


def scrape():
    return CBCCanadaScraper()()
