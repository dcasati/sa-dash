"""Calgary news scraper — CBC Calgary + Calgary Herald RSS."""
import requests
import feedparser
from src.scrape.base import BaseScraper, clean_text


# Multiple feeds for resilience
_FEEDS = [
    ("CBC Calgary", "https://www.cbc.ca/webfeed/rss/rss-canada-calgary"),
    ("Calgary Herald", "https://calgaryherald.com/feed"),
]


class CalgaryNewsScraper(BaseScraper):
    ID = "calgary_news"
    LABEL = "📰 Calgary News"
    SOURCE_URLS = [url for _, url in _FEEDS]

    def fetch(self) -> dict:
        all_items = []
        for name, url in _FEEDS:
            try:
                resp = requests.get(url, timeout=20, allow_redirects=True)
                resp.raise_for_status()
                feed = feedparser.parse(resp.text)
                for entry in feed.entries[:4]:
                    title = clean_text(getattr(entry, "title", "")) or "Untitled"
                    link = getattr(entry, "link", "") or ""
                    all_items.append({"title": title, "link": link, "source": name})
            except Exception:
                continue

        if all_items:
            items_html = []
            for e in all_items[:8]:
                items_html.append(
                    f'<li><a href="{e["link"]}">{e["title"]}</a> '
                    f'<span class="meta">({e["source"]})</span></li>'
                )
            html = f"<ul>{''.join(items_html)}</ul>"
            text = "; ".join(e["title"] for e in all_items[:8])
        else:
            html = '<p>News feeds temporarily unavailable. See <a href="https://www.cbc.ca/news/canada/calgary">CBC Calgary</a></p>'
            text = "News unavailable — see cbc.ca/news/canada/calgary"
        return self.result(html=html, text=text)


def scrape():
    return CalgaryNewsScraper()()
