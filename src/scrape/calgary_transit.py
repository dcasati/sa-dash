"""Calgary Transit info scraper."""
import requests
from src.scrape.base import BaseScraper

class CalgaryTransitScraper(BaseScraper):
    ID = "calgary_transit"
    LABEL = "🚇 Calgary Transit"
    SOURCE_URLS = ["https://www.calgarytransit.com/"]

    def fetch(self) -> dict:
        try:
            url = "https://data.calgary.ca/resource/4jhi-5m3j.json?$limit=5&$order=date DESC"
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200 and resp.json():
                alerts = resp.json()
                items = []
                for a in alerts[:5]:
                    desc = a.get("description", "Transit alert")[:100]
                    items.append(f"<li>{desc}</li>")
                html = f"<ul>{''.join(items)}</ul>" if items else "<p>No current transit alerts.</p>"
                text = "; ".join(a.get("description", "")[:80] for a in alerts[:5])
            else:
                html = "<p>Calgary Transit: No current alerts.</p>"
                text = "No current transit alerts."
        except Exception:
            html = "<p>Calgary Transit: Service info temporarily unavailable.</p>"
            text = "Transit info unavailable."
        return self.result(html=html, text=text)

def scrape():
    return CalgaryTransitScraper()()
