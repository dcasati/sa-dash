"""Weather scraper for Calgary using wttr.in + Environment Canada alerts."""
import requests
from src.scrape.base import BaseScraper


class WeatherCalgaryScraper(BaseScraper):
    ID = "weather_calgary"
    LABEL = "🌤️ Calgary Weather"
    SOURCE_URLS = [
        "https://wttr.in/Calgary",
        "https://weather.gc.ca/rss/battleboard/ab12_e.xml",
    ]

    def fetch(self) -> dict:
        # Current conditions from wttr.in
        weather_html = ""
        weather_text = ""
        try:
            resp = requests.get(
                "https://wttr.in/Calgary?format=%c+%t+|+Feels+like:+%f+|+Wind:+%w+|+Humidity:+%h+|+UV:+%u",
                headers={"User-Agent": "curl/8.0"},
                timeout=15,
            )
            resp.raise_for_status()
            current = resp.text.strip()

            # Also get a brief forecast
            resp2 = requests.get(
                "https://wttr.in/Calgary?format=%c+%t+%w",
                headers={"User-Agent": "curl/8.0"},
                timeout=15,
            )
            weather_html = f'<p><strong>Now:</strong> {current}</p>'
            weather_text = current
        except Exception:
            weather_html = "<p>Current weather temporarily unavailable.</p>"
            weather_text = "Weather unavailable."

        # Weather alerts from Environment Canada
        alerts_html = ""
        try:
            resp = requests.get(
                "https://weather.gc.ca/rss/battleboard/ab12_e.xml",
                timeout=15,
            )
            resp.raise_for_status()
            import xml.etree.ElementTree as ET

            root = ET.fromstring(resp.text)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            entries = root.findall("atom:entry", ns)
            if entries:
                for entry in entries[:3]:
                    title = entry.find("atom:title", ns)
                    summary = entry.find("atom:summary", ns)
                    title_text = title.text if title is not None else ""
                    if "no alerts" in title_text.lower():
                        alerts_html = '<p>✅ <em>No weather alerts in effect.</em></p>'
                    else:
                        summary_text = summary.text if summary is not None else ""
                        alerts_html += f"<p>⚠️ <strong>{title_text}</strong></p>"
                        if summary_text:
                            alerts_html += f"<p>{summary_text[:200]}</p>"
        except Exception:
            alerts_html = ""

        html = weather_html + alerts_html
        return self.result(html=html, text=weather_text)


def scrape():
    return WeatherCalgaryScraper()()
