"""General info panel for Calgary."""
import datetime as dt
import zoneinfo
from src.scrape.base import BaseScraper

MDT = zoneinfo.ZoneInfo("America/Edmonton")

class InfoCalgaryScraper(BaseScraper):
    ID = "info_calgary"
    LABEL = "ℹ️ Calgary Info"
    SOURCE_URLS = []

    def fetch(self) -> dict:
        now = dt.datetime.now(MDT)
        html = f"""<div class="info-panel">
<p><strong>Calgary, Alberta</strong> — Elevation: 1,045m | Pop: ~1.3M</p>
<p>Coordinates: 51.0447°N, 114.0719°W</p>
</div>"""
        text = "Calgary, AB — Elevation 1,045m, Pop ~1.3M, 51.0447°N 114.0719°W"
        return self.result(html=html, text=text)

def scrape():
    return InfoCalgaryScraper()()
