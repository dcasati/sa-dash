"""Calgary news scraper — CBC Calgary RSS feed."""
import requests
from src.scrape.base import BaseScraper, clean_text
from src.scrape.rss import parse_rss, render_rss_html


class CalgaryNewsScraper(BaseScraper):
    ID = "calgary_news"
    LABEL = "📰 Calgary News"
    SOURCE_URLS = ["https://www.cbc.ca/webfeed/rss/rss-canada-calgary"]

    def fetch(self) -> dict:
        url = "https://www.cbc.ca/webfeed/rss/rss-canada-calgary"
        try:
            resp = requests.get(url, timeout=20, allow_redirects=True)
            resp.raise_for_status()
            items = parse_rss(resp.text, limit=8)
            if items:
                html = render_rss_html(items)
                text = "; ".join(item["title"] for item in items)
            else:
                html = '<p>No recent Calgary news. <a href="https://www.cbc.ca/news/canada/calgary">CBC Calgary →</a></p>'
                text = "No recent news."
        except Exception:
            html = '<p>News feed temporarily unavailable. <a href="https://www.cbc.ca/news/canada/calgary">CBC Calgary →</a></p>'
            text = "News unavailable."
        return self.result(html=html, text=text)


def scrape():
    return CalgaryNewsScraper()()
