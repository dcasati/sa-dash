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
        # Current conditions + forecast from wttr.in JSON API (metric)
        weather_html = ""
        weather_text = ""
        try:
            resp = requests.get(
                "https://wttr.in/Calgary?format=j1&m",
                headers={"User-Agent": "curl/8.0"},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()

            # Current conditions
            cc = data["current_condition"][0]
            temp = cc["temp_C"]
            feels = cc["FeelsLikeC"]
            wind_speed = cc["windspeedKmph"]
            wind_dir = cc["winddir16Point"]
            humidity = cc["humidity"]
            uv = cc["uvIndex"]
            desc = cc["weatherDesc"][0]["value"]
            visibility = cc.get("visibility", "")

            weather_html = (
                f'<p><strong>Now:</strong> {desc} | <strong>{temp}°C</strong> '
                f'(feels {feels}°C) | Wind: {wind_speed} km/h {wind_dir} | '
                f'Humidity: {humidity}% | UV: {uv}</p>'
            )
            weather_text = f"{desc}, {temp}°C (feels {feels}°C), wind {wind_speed} km/h {wind_dir}"

            # 3-day forecast
            forecast_rows = []
            for day in data.get("weather", [])[:3]:
                date = day["date"]
                high = day["maxtempC"]
                low = day["mintempC"]
                # Get noon-ish description (index 4 = 12:00)
                hourly = day.get("hourly", [])
                noon = hourly[4] if len(hourly) > 4 else hourly[0] if hourly else None
                day_desc = noon["weatherDesc"][0]["value"] if noon else ""
                rain_mm = noon.get("precipMM", "0") if noon else "0"
                wind = noon.get("windspeedKmph", "") if noon else ""

                forecast_rows.append(
                    f'<tr><td>{date}</td><td>{day_desc}</td>'
                    f'<td><strong>{high}°C</strong> / {low}°C</td>'
                    f'<td>{wind} km/h</td><td>{rain_mm} mm</td></tr>'
                )

            if forecast_rows:
                weather_html += (
                    '<table class="info-table">'
                    '<tr><th>Date</th><th>Conditions</th><th>High/Low</th><th>Wind</th><th>Precip</th></tr>'
                    + "".join(forecast_rows) +
                    '</table>'
                )

        except Exception as e:
            import sys
            print(f"[weather_calgary] Error: {e}", file=sys.stderr)
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
