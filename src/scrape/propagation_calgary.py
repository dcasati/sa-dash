"""Radio propagation scraper for Calgary area using PSKReporter and solar data."""
import requests
from src.scrape.base import BaseScraper


_SOLAR_URL = "https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json"
_KINDEX_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"


class PropagationCalgaryScraper(BaseScraper):
    ID = "propagation_calgary"
    LABEL = "📻 Radio Propagation"
    SOURCE_URLS = [
        "https://www.hamqsl.com/solar.html",
        "https://pskreporter.info",
    ]

    def fetch(self) -> dict:
        parts = []

        # Solar/geomagnetic data from NOAA SWPC
        try:
            resp = requests.get(_KINDEX_URL, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            # data is a list of lists, first row is header
            if len(data) > 2:
                latest = data[-1]  # most recent entry
                # Format: [time_tag, Kp, Kp_fraction, a_running, station_count]
                kp = latest[1]
                time_tag = latest[0]
                kp_val = float(kp) if kp else 0

                if kp_val <= 2:
                    condition = "Quiet"
                    emoji = "🟢"
                elif kp_val <= 4:
                    condition = "Unsettled"
                    emoji = "🟡"
                elif kp_val <= 5:
                    condition = "Storm"
                    emoji = "🟠"
                else:
                    condition = "Major Storm"
                    emoji = "🔴"

                parts.append(
                    f'<p>{emoji} <strong>Geomagnetic: {condition}</strong> (Kp={kp}) — {time_tag}</p>'
                )
        except Exception:
            pass

        # Solar flux and sunspot data
        try:
            resp = requests.get(
                "https://services.swpc.noaa.gov/json/f107_cm_flux.json",
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            if data:
                latest = data[-1]
                flux = latest.get("flux", "N/A")
                parts.append(f'<p>☀️ Solar Flux Index (SFI): <strong>{flux}</strong></p>')
        except Exception:
            pass

        # Band conditions summary
        try:
            resp = requests.get(
                "https://www.hamqsl.com/solarxml.php",
                timeout=15,
            )
            resp.raise_for_status()
            import xml.etree.ElementTree as ET
            root = ET.fromstring(resp.text)
            sc = root.find(".//solardata")
            if sc is not None:
                sn = sc.find("sunspots")
                sfi = sc.find("solarflux")
                sig = sc.find("signalnoise")
                if sn is not None:
                    parts.append(f"<p>Sunspots: {sn.text} | SFI: {sfi.text if sfi is not None else 'N/A'} | Signal Noise: {sig.text if sig is not None else 'N/A'}</p>")

                # Band conditions
                bands = root.findall(".//calculatedconditions/band")
                if bands:
                    rows = []
                    for b in bands:
                        name = b.get("name", "?")
                        time_attr = b.get("time", "")
                        cond = b.text or "N/A"
                        rows.append(f"<tr><td>{name}</td><td>{time_attr}</td><td>{cond}</td></tr>")
                    parts.append(
                        '<table class="info-table"><tr><th>Band</th><th>Time</th><th>Condition</th></tr>'
                        + "".join(rows)
                        + "</table>"
                    )
        except Exception:
            pass

        if not parts:
            parts.append(
                '<p>Propagation data temporarily unavailable. '
                'See <a href="https://www.hamqsl.com/solar.html">hamqsl.com</a></p>'
            )

        parts.append(
            '<p class="meta">'
            '<a href="https://pskreporter.info/pskmap.html?preset&callsign=VE6&what=all&mode=ALL">PSKReporter (VE6) →</a> | '
            '<a href="https://www.hamqsl.com/solar.html">Solar Conditions →</a>'
            '</p>'
        )

        html = "".join(parts)
        text = "Radio propagation conditions — see hamqsl.com/solar.html"
        return self.result(html=html, text=text)


def scrape():
    return PropagationCalgaryScraper()()
