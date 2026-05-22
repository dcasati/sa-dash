"""Weather scraper for Calgary using Environment Canada."""
import datetime as dt
import zoneinfo
import requests
from src.scrape.base import BaseScraper

MDT = zoneinfo.ZoneInfo("America/Edmonton")

class WeatherCalgaryScraper(BaseScraper):
    ID = "weather_calgary"
    LABEL = "🌤️ Calgary Weather"
    SOURCE_URLS = ["https://weather.gc.ca/city/pages/ab-52_metric_e.html"]

    def fetch(self) -> dict:
        url = "https://dd.weather.gc.ca/citypage_weather/xml/AB/s0000047_e.xml"
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        import xml.etree.ElementTree as ET
        root = ET.fromstring(resp.text)
        
        cc = root.find(".//currentConditions")
        if cc is None:
            return self.result(html="<p>Weather data temporarily unavailable.</p>", text="Weather data unavailable.")
        
        temp_el = cc.find("temperature")
        temp = temp_el.text if temp_el is not None else "N/A"
        condition_el = cc.find("condition")
        condition = condition_el.text if condition_el is not None else "N/A"
        wind_speed_el = cc.find(".//wind/speed")
        wind_speed = wind_speed_el.text if wind_speed_el is not None else "N/A"
        wind_dir_el = cc.find(".//wind/direction")
        wind_dir = wind_dir_el.text if wind_dir_el is not None else ""
        humidity_el = cc.find("relativeHumidity")
        humidity = humidity_el.text if humidity_el is not None else "N/A"
        
        html = f"""<div class="weather-current">
<p><strong>{condition}</strong> — {temp}°C</p>
<p>Wind: {wind_dir} {wind_speed} km/h | Humidity: {humidity}%</p>
</div>"""
        text = f"{condition}, {temp}°C, Wind {wind_dir} {wind_speed} km/h, Humidity {humidity}%"
        return self.result(html=html, text=text)

def scrape():
    return WeatherCalgaryScraper()()
