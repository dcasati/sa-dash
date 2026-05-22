"""Calgary traffic conditions scraper."""
import requests
from src.scrape.base import BaseScraper

class CalgaryTrafficScraper(BaseScraper):
    ID = "calgary_traffic"
    LABEL = "🚗 Traffic"
    SOURCE_URLS = ["https://data.calgary.ca/"]

    def fetch(self) -> dict:
        try:
            url = "https://data.calgary.ca/resource/35ra-9556.json?$limit=8&$order=start_dt DESC"
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200 and resp.json():
                events = resp.json()
                items = []
                for e in events[:8]:
                    desc = e.get("description", "Traffic event")[:120]
                    items.append(f"<li>{desc}</li>")
                html = f"<ul>{''.join(items)}</ul>"
                text = "; ".join(e.get("description", "")[:80] for e in events[:5])
            else:
                html = "<p>No current traffic incidents reported.</p>"
                text = "No traffic incidents."
        except Exception:
            html = "<p>Traffic data temporarily unavailable.</p>"
            text = "Traffic data unavailable."
        return self.result(html=html, text=text)

def scrape():
    return CalgaryTrafficScraper()()
