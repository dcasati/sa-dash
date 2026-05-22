"""Calgary news scraper via CBC RSS."""
import requests
from src.scrape.base import BaseScraper
from src.scrape.rss import parse_rss_entries

class CalgaryNewsScraper(BaseScraper):
    ID = "calgary_news"
    LABEL = "📰 Calgary News"
    SOURCE_URLS = ["https://www.cbc.ca/cmlink/rss-canada-calgary"]

    def fetch(self) -> dict:
        url = "https://www.cbc.ca/cmlink/rss-canada-calgary"
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            entries = parse_rss_entries(resp.text, limit=6)
            if entries:
                items = [f'<li><a href="{e["link"]}">{e["title"]}</a></li>' for e in entries]
                html = f"<ul>{''.join(items)}</ul>"
                text = "; ".join(e["title"] for e in entries)
            else:
                html = "<p>No recent Calgary news.</p>"
                text = "No recent news."
        except Exception:
            html = "<p>News feed temporarily unavailable.</p>"
            text = "News unavailable."
        return self.result(html=html, text=text)

def scrape():
    return CalgaryNewsScraper()()
