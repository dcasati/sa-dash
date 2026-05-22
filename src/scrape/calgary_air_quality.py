"""Calgary air quality scraper."""
import requests
from src.scrape.base import BaseScraper

class CalgaryAirQualityScraper(BaseScraper):
    ID = "calgary_air_quality"
    LABEL = "💨 Air Quality"
    SOURCE_URLS = ["https://airquality.alberta.ca/"]

    def fetch(self) -> dict:
        try:
            url = "https://data.calgary.ca/resource/uqjm-jxgc.json?$limit=3&$order=date_time DESC"
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200 and resp.json():
                data = resp.json()
                items = []
                for d in data[:3]:
                    aqhi = d.get("aqhi", "N/A")
                    station = d.get("station_name", "Calgary")
                    items.append(f"<li>{station}: AQHI {aqhi}</li>")
                html = f"<ul>{''.join(items)}</ul>"
                text = "; ".join(f"{d.get('station_name','Calgary')}: AQHI {d.get('aqhi','N/A')}" for d in data[:3])
            else:
                html = "<p>Air Quality: Check <a href='https://airquality.alberta.ca/'>airquality.alberta.ca</a></p>"
                text = "Air quality: see airquality.alberta.ca"
        except Exception:
            html = "<p>Air quality data temporarily unavailable.</p>"
            text = "Air quality data unavailable."
        return self.result(html=html, text=text)

def scrape():
    return CalgaryAirQualityScraper()()
