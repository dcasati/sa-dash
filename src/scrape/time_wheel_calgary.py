"""Time wheel scraper for Calgary."""
import datetime as dt
import zoneinfo
from src.scrape.base import BaseScraper

MDT = zoneinfo.ZoneInfo("America/Edmonton")

class TimeWheelCalgaryScraper(BaseScraper):
    ID = "time_wheel_calgary"
    LABEL = "🕐 Time Wheel"
    SOURCE_URLS = []

    def fetch(self) -> dict:
        now = dt.datetime.now(MDT)
        sunrise = "~05:40"
        sunset = "~21:20"
        html = f"""<div class="time-wheel">
<p><strong>{now.strftime('%A, %B %d, %Y')}</strong></p>
<p>{now.strftime('%H:%M %Z')} | Sunrise {sunrise} | Sunset {sunset}</p>
</div>"""
        text = f"{now.strftime('%A %B %d %Y %H:%M %Z')} | Sunrise {sunrise} | Sunset {sunset}"
        return self.result(html=html, text=text)

def scrape():
    return TimeWheelCalgaryScraper()()
