"""Calgary Emergency Management Agency (CEMA) alerts and city safety notices."""
import requests
from src.scrape.base import BaseScraper, clean_text
from src.scrape.rss import parse_rss, render_rss_html


# City of Calgary newsroom feeds for emergency-relevant info
_FEEDS = [
    ("https://newsroom.calgary.ca/tagfeed/en/tags/emergency", "Emergency"),
    ("https://newsroom.calgary.ca/tagfeed/en/tags/fire", "Fire"),
    ("https://newsroom.calgary.ca/tagfeed/en/tags/city__news", "City News"),
]


class CalgaryEmergencyScraper(BaseScraper):
    ID = "calgary_emergency"
    LABEL = "🚨 Emergency & City Alerts"
    SOURCE_URLS = [
        "https://www.calgary.ca/safety/staying-informed.html",
        "https://newsroom.calgary.ca",
    ]

    def fetch(self) -> dict:
        all_items = []

        for url, source_name in _FEEDS:
            try:
                resp = requests.get(url, timeout=15, allow_redirects=True)
                resp.raise_for_status()
                items = parse_rss(resp.text, limit=3)
                for item in items:
                    item["source"] = source_name
                all_items.extend(items)
            except Exception:
                continue

        if not all_items:
            html = (
                '<p>No current emergency alerts. '
                '<a href="https://www.calgary.ca/safety/staying-informed.html">'
                'Stay Informed (CEMA) →</a></p>'
            )
            text = "No current emergency alerts."
            return self.result(html=html, text=text)

        # Deduplicate by title and take the most recent items
        seen = set()
        unique = []
        for item in all_items:
            if item["title"] not in seen:
                seen.add(item["title"])
                unique.append(item)

        # Render top items
        html = render_rss_html(unique[:6])
        html += (
            '<p class="meta"><a href="https://www.calgary.ca/safety/staying-informed.html">'
            'CEMA - Stay Informed →</a></p>'
        )
        text = "; ".join(item["title"] for item in unique[:6])
        return self.result(html=html, text=text)


def scrape():
    return CalgaryEmergencyScraper()()
