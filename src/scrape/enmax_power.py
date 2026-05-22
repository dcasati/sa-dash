"""ENMAX power info for Calgary."""
from src.scrape.base import BaseScraper

class EnmaxPowerScraper(BaseScraper):
    ID = "enmax_power"
    LABEL = "⚡ ENMAX Power"
    SOURCE_URLS = ["https://www.enmax.com/outages"]

    def fetch(self) -> dict:
        html = '<p>Power status: <a href="https://www.enmax.com/outages">Check ENMAX outage map</a></p>'
        text = "Power: Check enmax.com/outages for current status."
        return self.result(html=html, text=text)

def scrape():
    return EnmaxPowerScraper()()
