"""Calgary river level scraper (Bow & Elbow rivers)."""
import requests
from src.scrape.base import BaseScraper

class CalgaryRiverLevelsScraper(BaseScraper):
    ID = "calgary_river_levels"
    LABEL = "🌊 River Levels"
    SOURCE_URLS = ["https://rivers.alberta.ca/"]

    def fetch(self) -> dict:
        try:
            # Alberta Rivers API for Bow River at Calgary
            url = "https://data.calgary.ca/resource/5fdg-ifgr.json?$limit=5&$order=timestamp DESC"
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200 and resp.json():
                data = resp.json()
                items = []
                for d in data[:3]:
                    level = d.get("level", "N/A")
                    station = d.get("station_name", "Station")
                    items.append(f"<li>{station}: {level}m</li>")
                html = f"<ul>{''.join(items)}</ul>"
                text = "; ".join(f"{d.get('station_name','')}: {d.get('level','')}m" for d in data[:3])
            else:
                html = "<p>River level data: Check <a href='https://rivers.alberta.ca/'>rivers.alberta.ca</a></p>"
                text = "River levels: see rivers.alberta.ca"
        except Exception:
            html = "<p>River level data temporarily unavailable. See <a href='https://rivers.alberta.ca/'>rivers.alberta.ca</a></p>"
            text = "River levels unavailable."
        return self.result(html=html, text=text)

def scrape():
    return CalgaryRiverLevelsScraper()()
