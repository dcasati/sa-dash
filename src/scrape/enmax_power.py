"""ENMAX power outage scraper for Calgary."""
import os
import requests
from src.scrape.base import BaseScraper


_OUTAGE_API_BASE = "https://epc-outagedatacache.azurewebsites.net/api/cache"


class EnmaxPowerScraper(BaseScraper):
    ID = "enmax_power"
    LABEL = "⚡ ENMAX Power"
    SOURCE_URLS = ["https://outages.enmax.com"]

    def fetch(self) -> dict:
        code = os.environ.get("ENMAX_OUTAGE_CODE", "")
        if not code:
            html = (
                '<p>Power outage data unavailable (no API key). '
                '<a href="https://outages.enmax.com">View ENMAX Outage Portal →</a></p>'
            )
            return self.result(html=html, text="See outages.enmax.com")

        try:
            resp = requests.get(f"{_OUTAGE_API_BASE}?code={code}", timeout=15)
            resp.raise_for_status()
            data = resp.json()

            if not data or (isinstance(data, list) and len(data) == 0):
                html = '<p>✅ No current power outages reported. <a href="https://outages.enmax.com">Outage map</a></p>'
                text = "No power outages reported."
                return self.result(html=html, text=text)

            # data is a list of outage objects
            outages = data if isinstance(data, list) else data.get("outages", [])
            total = len(outages)
            total_affected = sum(int(o.get("customersAffected", 0) or 0) for o in outages)

            items = []
            for o in outages[:8]:
                area = o.get("area", o.get("municipality", "Unknown area"))
                customers = o.get("customersAffected", "?")
                cause = o.get("cause", "Unknown")
                status = o.get("status", "")
                etr = o.get("estimatedRestoreTime", o.get("etr", ""))
                line = f"<li><strong>{area}</strong> — {customers} affected"
                if cause and cause != "Unknown":
                    line += f" | Cause: {cause}"
                if etr:
                    line += f" | ETR: {etr}"
                if status:
                    line += f" | {status}"
                line += "</li>"
                items.append(line)

            summary = f"<p><strong>{total} outage{'s' if total != 1 else ''}</strong> — {total_affected:,} customers affected</p>"
            html = summary + f"<ul>{''.join(items)}</ul>"
            if total > 8:
                html += f'<p><a href="https://outages.enmax.com">View all {total} outages →</a></p>'
            text = f"{total} outages, {total_affected} customers affected"
            return self.result(html=html, text=text)

        except Exception as e:
            import sys
            print(f"[enmax_power] API error: {e}", file=sys.stderr)
            # API is IP-restricted; show helpful fallback with direct link
            html = (
                '<p>⚡ Check ENMAX for current outages in your area:</p>'
                '<ul>'
                '<li><a href="https://outages.enmax.com">🗺️ ENMAX Outage Map</a> — live map & list view</li>'
                '<li><a href="tel:+14035142100">📞 403-514-2100</a> — report or check outages</li>'
                '</ul>'
            )
            text = "Check outages.enmax.com or call 403-514-2100"
            return self.result(html=html, text=text)


def scrape():
    return EnmaxPowerScraper()()
