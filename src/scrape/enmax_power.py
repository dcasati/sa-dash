"""ENMAX power outage scraper for Calgary via poweroutage.com."""
import requests
from bs4 import BeautifulSoup
from src.scrape.base import BaseScraper


_POWER_URL = "https://poweroutage.com/ca/utility/1507"


class EnmaxPowerScraper(BaseScraper):
    ID = "enmax_power"
    LABEL = "⚡ ENMAX Power"
    SOURCE_URLS = [_POWER_URL]

    def fetch(self) -> dict:
        try:
            resp = requests.get(_POWER_URL, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            # Extract summary stats from the top area
            total_tracked = ""
            total_out = ""
            last_updated = ""

            # Look for key stats in text
            text_content = soup.get_text()
            for line in text_content.split("\n"):
                line = line.strip()
                if "Utility Outages" in line or "Customers Out" in line:
                    pass  # header labels

            # Parse the county table
            rows = []
            table_links = soup.find_all("a", href=True)
            counties = []
            for link in table_links:
                if "/ca/county/" in link.get("href", ""):
                    counties.append(link.get_text(strip=True))

            # Try to get structured data from the page
            # The page has: Customers Tracked, Utility Outages, table with county/tracked/out
            numbers = []
            for el in soup.find_all(string=True):
                t = el.strip()
                if t and t.replace(",", "").isdigit():
                    numbers.append(t)

            # Parse: first number = customers tracked, second = utility outages
            customers_tracked = numbers[0] if len(numbers) > 0 else "?"
            utility_outages = numbers[1] if len(numbers) > 1 else "?"

            # Build county table from remaining numbers (pairs: tracked, out)
            county_data = []
            idx = 2  # skip first two summary numbers
            for county in counties:
                tracked = numbers[idx] if idx < len(numbers) else "?"
                out = numbers[idx + 1] if idx + 1 < len(numbers) else "?"
                county_data.append((county, tracked, out))
                idx += 2

            # Determine if there are outages
            try:
                outage_count = int(str(utility_outages).replace(",", ""))
            except (ValueError, TypeError):
                outage_count = 0

            if outage_count == 0:
                html = (
                    f'<p>✅ <strong>No current outages</strong> — '
                    f'{customers_tracked} customers tracked</p>'
                )
                if county_data:
                    html += '<table class="info-table"><tr><th>Area</th><th>Tracked</th><th>Out</th></tr>'
                    for county, tracked, out in county_data:
                        html += f'<tr><td>{county}</td><td>{tracked}</td><td>{out}</td></tr>'
                    html += '</table>'
                html += f'<p><small>Source: <a href="{_POWER_URL}">poweroutage.com</a></small></p>'
                text = f"No outages — {customers_tracked} customers tracked"
            else:
                html = (
                    f'<p>⚠️ <strong>{utility_outages} outage{"s" if outage_count != 1 else ""}</strong> — '
                    f'{customers_tracked} customers tracked</p>'
                )
                if county_data:
                    html += '<table class="info-table"><tr><th>Area</th><th>Tracked</th><th>Out</th></tr>'
                    for county, tracked, out in county_data:
                        style = ' style="color:#e74c3c;font-weight:bold"' if out != "0" else ""
                        html += f'<tr><td>{county}</td><td>{tracked}</td><td{style}>{out}</td></tr>'
                    html += '</table>'
                html += f'<p><small>Source: <a href="{_POWER_URL}">poweroutage.com</a></small></p>'
                text = f"{utility_outages} outages across ENMAX service area"

            return self.result(html=html, text=text)

        except Exception as e:
            import sys
            print(f"[enmax_power] Error: {e}", file=sys.stderr)
            html = (
                f'<p>⚡ <a href="{_POWER_URL}">Check ENMAX outages on poweroutage.com →</a></p>'
            )
            return self.result(html=html, text="See poweroutage.com for ENMAX status")


def scrape():
    return EnmaxPowerScraper()()
