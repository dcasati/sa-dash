"""Time wheel scraper for Calgary with timezone conversion."""
import datetime as dt
import zoneinfo
from src.scrape.base import BaseScraper

MDT = zoneinfo.ZoneInfo("America/Edmonton")
UTC = dt.timezone.utc


class TimeWheelCalgaryScraper(BaseScraper):
    ID = "time_wheel_calgary"
    LABEL = "🕐 Timezones (MDT↔UTC)"
    SOURCE_URLS = []

    def fetch(self) -> dict:
        now = dt.datetime.now(MDT)
        now_utc = now.astimezone(UTC)

        # Build a simple timezone comparison table (next 24h)
        rows_utc = []
        rows_mdt = []
        for h in range(24):
            utc_hour = (now_utc.hour + h) % 24
            mdt_hour = (now.hour + h) % 24
            rows_utc.append(str(utc_hour).zfill(2))
            rows_mdt.append(str(mdt_hour).zfill(2))

        utc_row = "".join(f"<td>{h}</td>" for h in rows_utc[:13])
        mdt_row = "".join(f"<td>{h}</td>" for h in rows_mdt[:13])

        offset = now.strftime('%z')
        offset_str = f"UTC{offset[:3]}:{offset[3:]}"

        html = f"""<div class="time-wheel">
<p><strong>{now.strftime('%A, %B %d, %Y')}</strong></p>
<p>{now.strftime('%H:%M %Z')} ({offset_str}) | UTC: {now_utc.strftime('%H:%M')}</p>
<table class="tz-table">
<tr><td>UTC</td>{utc_row}</tr>
<tr><td>MDT</td>{mdt_row}</tr>
</table>
</div>"""
        text = f"{now.strftime('%A %B %d %Y %H:%M %Z')} | UTC: {now_utc.strftime('%H:%M')}"
        return self.result(html=html, text=text)


def scrape():
    return TimeWheelCalgaryScraper()()
