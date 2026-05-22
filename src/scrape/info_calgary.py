"""General info panel for Calgary — contacts, radio, and key resources."""
import datetime as dt
import zoneinfo
from src.scrape.base import BaseScraper

MDT = zoneinfo.ZoneInfo("America/Edmonton")


class InfoCalgaryScraper(BaseScraper):
    ID = "info_calgary"
    LABEL = "ℹ️ Info (Contacts & Radio)"
    SOURCE_URLS = []

    def fetch(self) -> dict:
        now = dt.datetime.now(MDT)
        html = """<div class="info-panel">
<h3>Calgary Info</h3>
<p><strong>Calgary, Alberta</strong> — Elevation: 1,045m | Pop: ~1.3M | Coordinates: 51.0447°N, 114.0719°W</p>

<h3>Emergency & City Contacts</h3>
<table class="info-table">
<tr><td>Emergency</td><td><a href="tel:911">911</a></td><td>Police, Fire, EMS</td></tr>
<tr><td>Calgary Police (non-emergency)</td><td><a href="tel:+14032661234">403-266-1234</a></td><td><a href="https://www.calgarypolice.ca">calgarypolice.ca</a></td></tr>
<tr><td>Calgary Fire Dept</td><td><a href="tel:+14032687200">403-268-7200</a></td><td>Non-emergency</td></tr>
<tr><td>CEMA (Emergency Mgmt)</td><td><a href="tel:+14032688200">403-268-8200</a></td><td><a href="https://www.calgary.ca/safety">calgary.ca/safety</a></td></tr>
<tr><td>Alberta Emergency Alert</td><td></td><td><a href="https://www.alberta.ca/emergency">alberta.ca/emergency</a></td></tr>
<tr><td>ENMAX (power emergency)</td><td><a href="tel:+14035142100">403-514-2100</a></td><td><a href="https://outages.enmax.com">outages.enmax.com</a></td></tr>
<tr><td>City of Calgary 311</td><td><a href="tel:311">311</a></td><td>City services, road hazards, water issues</td></tr>
<tr><td>Alberta Health Link</td><td><a href="tel:811">811</a></td><td>Health advice 24/7</td></tr>
<tr><td>Poison Centre</td><td><a href="tel:+18033221414">1-800-332-1414</a></td><td>Alberta Poison & Drug Info</td></tr>
<tr><td>Distress Centre Calgary</td><td><a href="tel:+14032660066">403-266-HELP (4357)</a></td><td>24/7 crisis line</td></tr>
<tr><td>Foothills Medical Centre</td><td><a href="tel:+14039441110">403-944-1110</a></td><td>Trauma centre</td></tr>
<tr><td>Rockyview General Hospital</td><td><a href="tel:+14039431110">403-943-3000</a></td><td></td></tr>
<tr><td>Alberta Wildfire Status</td><td></td><td><a href="https://www.albertafirestatus.ca">albertafirestatus.ca</a></td></tr>
<tr><td>511 Alberta (roads)</td><td><a href="tel:511">511</a></td><td><a href="https://511.alberta.ca">511.alberta.ca</a></td></tr>
<tr><td>River Conditions</td><td></td><td><a href="https://rivers.alberta.ca">rivers.alberta.ca</a></td></tr>
</table>

<details>
<summary><strong>📻 Radio Information</strong> (Broadcast, Amateur, Winlink)</summary>

<h3>Broadcast Radio</h3>
<table class="info-table">
<tr><th>Station</th><th>Freq</th><th>Band</th><th>Format</th></tr>
<tr><td>CBC Radio One</td><td>99.1</td><td>FM</td><td>News/Talk (EAS)</td></tr>
<tr><td>660 News</td><td>660</td><td>AM</td><td>All News</td></tr>
<tr><td>770 CHQR</td><td>770</td><td>AM</td><td>News/Talk</td></tr>
<tr><td>QR77</td><td>770</td><td>AM</td><td>Talk</td></tr>
<tr><td>CFFR</td><td>660</td><td>AM</td><td>News</td></tr>
<tr><td>Environment Canada WX</td><td>162.475</td><td>VHF</td><td>Weather (24/7)</td></tr>
</table>

<h3>Amateur Radio</h3>
<p>National calling: 146.520 MHz FM | GMRS calling: 462.675 MHz (CH 20)</p>
<table class="info-table">
<tr><th>Call</th><th>Freq (MHz)</th><th>Offset</th><th>Tone</th><th>Site</th></tr>
<tr><td>VE6RYC</td><td>146.940</td><td>−</td><td>100.0</td><td>Nose Hill, Calgary</td></tr>
<tr><td>VE6RCR</td><td>147.150</td><td>+</td><td>100.0</td><td>Broadcast Hill</td></tr>
<tr><td>VE6OC</td><td>146.760</td><td>−</td><td>100.0</td><td>Calgary Centre</td></tr>
<tr><td>VE6CRC</td><td>146.820</td><td>−</td><td>100.0</td><td>Cochrane</td></tr>
<tr><td>VE6KAM</td><td>145.470</td><td>−</td><td>100.0</td><td>ARES Calgary</td></tr>
<tr><td>VE6OIL</td><td>146.670</td><td>−</td><td>100.0</td><td>Calgary ACS (Voice)</td></tr>
<tr><td>VE6REP</td><td>443.100</td><td>+</td><td>100.0</td><td>UHF Calgary</td></tr>
<tr><td>VE6YYC</td><td>444.225</td><td>+</td><td>100.0</td><td>DMR Calgary</td></tr>
</table>
<p><em>Calgary ARES: <a href="https://www.calgaryares.ca">calgaryares.ca</a> | RAC: <a href="https://www.rac.ca">rac.ca</a></em></p>

<h3>Winlink Gateway</h3>
<p>RMS stations within range of Calgary (HF, VHF & UHF):</p>
<table class="info-table">
<tr><th>Call</th><th>Freq</th><th>Mode</th><th>Grid</th></tr>
<tr><td>VE6KTL-10</td><td>145.010</td><td>Packet</td><td>DO21</td></tr>
<tr><td>VE6WMA-10</td><td>145.030</td><td>Packet</td><td>DO21</td></tr>
<tr><td>VE6HRR-5</td><td>7083.5</td><td>VARA HF</td><td>DO20</td></tr>
<tr><td>VE6FAR</td><td>UHF</td><td>VARA / Packet</td><td></td></tr>
<tr><td>VE6SRC</td><td>HF / VHF</td><td>VARA / Packet</td><td></td></tr>
</table>
</details>
</div>"""
        text = "Calgary, AB — 51.0447°N 114.0719°W — Emergency: 911, Non-emerg Police: 403-266-1234, CEMA: 403-268-8200"
        return self.result(html=html, text=text)


def scrape():
    return InfoCalgaryScraper()()
